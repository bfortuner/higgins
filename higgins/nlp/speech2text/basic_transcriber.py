import logging
from typing import Iterable

import speech_recognition as sr

from .audio_transcriber import AudioTranscriber, AudioTranscript


class BasicTranscriber(AudioTranscriber):
    """Parse audio from microphone using Speech Recognition library.

    This class transcribes microphone audio to text. In the future, we
    should also support pre-recorded audio files for integration tests.
    """
    def __init__(self):
        self.recognizer = sr.Recognizer()

        logging.info("Calibrating microphone. Be quiet..")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def listen(self) -> Iterable[AudioTranscript]:
        try:
            with sr.Microphone() as source:
                logging.info("Listening...")
                audio = self.recognizer.listen(source)
                logging.info("Recognizing...")
                text = self.recognizer.recognize_google(audio)
                return [AudioTranscript(text, is_final=True)]
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        raise Exception("Failed to capture audio and perform speech recognition")
