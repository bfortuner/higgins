"""Using Porcupine for wake word detection.

https://github.com/Picovoice/porcupine
https://github.com/Picovoice/picovoice
"""

import os
import struct
from datetime import datetime
from threading import Thread
from typing import List

import pvporcupine
import pyaudio

from higgins.const import WAKE_WORDS, WAKE_WORD_PATHS


class WakeWordDetected(Exception):
    pass


class WakeWordDetector(Thread):
    """Based on Porcupine Python Demo.

    https://github.com/Picovoice/porcupine
    """
    def __init__(
        self,
        keywords=None,
        keyword_paths=None,
        exit_on_wake=False,
        library_path=pvporcupine.LIBRARY_PATH,
        model_path=None,
        sensitivities=None,
        input_device_index=None,
    ):
        """
        Constructor.

        :param keywords: Built-in wake words like "Higgins" or "Hey google"
        :param keyword_paths: Absolute paths to keyword model files.
        :param exit_on_wake: Return if wake word detected, otherwise print detections. Default False.
        :param library_path: Absolute path to Porcupine's dynamic library.
        :param model_path: Absolute path to the file containing model parameters.
        :param sensitivities: Sensitivities for detecting keywords. Each value should be a number within [0, 1]. A
        higher sensitivity results in fewer misses at the cost of increasing the false alarm rate. If not set 0.5 will
        be used.
        :param input_device_index: Optional argument. If provided, audio is recorded from this input device. Otherwise,
        the default audio input device is used.
        """
        super().__init__()
        self._keyword_paths = self._get_keyword_paths(keywords, keyword_paths)
        self._exit_on_wake = exit_on_wake
        self._library_path = library_path
        self._model_path = model_path
        self._sensitivities = sensitivities
        self._input_device_index = input_device_index

    @classmethod
    def show_audio_devices(cls):
        fields = ('index', 'name', 'defaultSampleRate', 'maxInputChannels')
        pa = pyaudio.PyAudio()
        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            print(', '.join("'%s': '%s'" % (k, str(info[k])) for k in fields))
        pa.terminate()

    def _get_keyword_paths(self, keywords, keyword_paths):
        if keyword_paths is None:
            if keywords is None:
                raise ValueError("Either `keywords` or `keyword_paths` must be set.")
            keyword_paths = [pvporcupine.KEYWORD_PATHS[x] for x in keywords]
        return keyword_paths

    def run(self):
        """Listen for wake word and exit or print.

        Creates an input audio stream, instantiates an instance of Porcupine object, and monitors the audio stream for
        occurrences of the wake word(s). It prints the time of detection for each occurrence and the wake word.
        """
        keywords = list()
        for x in self._keyword_paths:
            keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
            if len(keyword_phrase_part) > 6:
                keywords.append(' '.join(keyword_phrase_part[0:-6]))
            else:
                keywords.append(keyword_phrase_part[0])

        porcupine = None
        pa = None
        audio_stream = None
        try:
            porcupine = pvporcupine.create(
                library_path=self._library_path,
                model_path=self._model_path,
                keyword_paths=self._keyword_paths,
                sensitivities=self._sensitivities)

            pa = pyaudio.PyAudio()

            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length,
                input_device_index=self._input_device_index)

            print('Listening {')
            for keyword, sensitivity in zip(keywords, self._sensitivities):
                print('  %s (%.2f)' % (keyword, sensitivity))
            print('}')

            while True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                result = porcupine.process(pcm)
                if result >= 0:
                    msg = "[%s] Detected %s" % (str(datetime.now()), keywords[result])
                    print(msg)
                    if self._exit_on_wake:
                        raise WakeWordDetected()

        except WakeWordDetected:
            pass
        finally:
            if porcupine is not None:
                porcupine.delete()

            if audio_stream is not None:
                audio_stream.close()

            if pa is not None:
                pa.terminate()


def listen_for_wake_word(
    wake_words: List[str] = WAKE_WORDS,
    wake_word_paths: List[str] = WAKE_WORD_PATHS
):
    print(WakeWordDetector.show_audio_devices())
    if wake_word_paths and os.path.exists(wake_word_paths[0]):
        print(f"Found custom wake word model: {wake_word_paths}")
        wake_words = None
    else:
        wake_word_paths = None

    detector = WakeWordDetector(
        keywords=wake_words,
        keyword_paths=wake_word_paths,
        exit_on_wake=True,
        sensitivities=[.5],
        input_device_index=None,
    )
    detector.run()
