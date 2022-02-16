import logging
import time
from typing import Iterable, List

from google.cloud import speech
from google.cloud.speech import StreamingRecognizeResponse


from higgins.const import SILENCE_TIMEOUT_SEC
from higgins.devices.microphone import MicrophoneStream
from higgins.nlp import nlp_utils

from .audio_transcriber import AudioTranscriber, AudioTranscript

# Audio recording parameters
RATE = 16000  # Frames per second
CHUNK = int(RATE / 10)  # Buffer length - Number of frames to accumulate before returning audio
LANGUAGE_CODE = "en-US"

logger = logging.getLogger(__name__)


def _get_speech_contexts(supported_commands):
    """Tell Google about phrases we expect to improve transcription quality.

    https://cloud.google.com/speech-to-text/docs/speech-adaptation
    """
    contexts = []

    # Add the hard-coded leaf-node commands
    contexts.append(speech.SpeechContext(phrases=supported_commands))

    # Add common command prefixes and keywords
    prefixes = [
        "click",
        "go to",
        "launch",
        "switch to",
        "open",
        "Chrome",
        "Spotify",
        "code",
        "terminal",
        "new"
    ]
    contexts.append(speech.SpeechContext(phrases=prefixes))

    return contexts


class GoogleTranscriber(AudioTranscriber):
    """Parse audio from microphone using Google Cloud Speech API.

    This class transcribes microphone audio to text. In the future, we
    should also support pre-recorded audio files for integration tests.
    """
    def __init__(self, supported_commands: List[str] = None, single_utterance: bool = True):
        """Instantiate the Listener.

        Args:
            supported_commands: Optional; A hard-coded list of text commands. If we detect
                one of these phrases during transcription, we can exit early and return the phrase,
                instead of waiting for Google to detect that the user has stopped speaking. This noticeably
                speeds up transcription times for known phrases (Brendan).
            single_utterance: Optional; indicates whether this request should automatically end after speech
                is no longer detected. If set, Speech-to-Text will detect pauses, silence, or non-speech audio
                to determine when to end recognition.
        """
        self.supported_commands = supported_commands or []
        self._client = speech.SpeechClient()
        self._config = speech.StreamingRecognitionConfig(
            config=speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=RATE,
                language_code=LANGUAGE_CODE,
                model="command_and_search",  # Recommended for short commands
                speech_contexts=_get_speech_contexts(supported_commands)
            ),
            interim_results=True,
            single_utterance=single_utterance
        )

    def listen(self) -> AudioTranscript:
        """Record and transcribe user utterance using Microphone.

        Returns:
            AudioTranscript with detected utterance and additional metadata.
        """
        with MicrophoneStream(rate=RATE, chunk=CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )
            responses = self._client.streaming_recognize(self._config, requests)
            transcriptions = _handle_transcription_stream(responses, self.supported_commands)
            is_final = False
            while not is_final:
                transcript = next(transcriptions)
                is_final = transcript.is_final
                yield transcript


def _is_supported_command(text: str, supported_commands: List[str]) -> bool:
    return nlp_utils.normalize_text(text) in supported_commands


def _handle_transcription_stream(
    responses: Iterable[StreamingRecognizeResponse], supported_commands: List[str], deadline: int = SILENCE_TIMEOUT_SEC
) -> Iterable[AudioTranscript]:
    """Handle streaming transcriptions from Google Cloud Speech API.

    Args:
        responses: Iterable of Google API responses
        supported_commands: Optional; A hard-coded list of text commands. If we detect
            one of these phrases during transcription, we can exit early and return the phrase,
            instead of waiting for Google to detect that the user has stopped speaking.
        deadline: Optional; Maximum amount of seconds to wait for user to say something, otherwise
            exit early due to inactivity. NOTE: Google currently controls part of this equation,
            since they wait for silence on their end, too. So even with a deadline=0, we would still
            wait for N seconds for google to detect the silence and send an end of utterance event.

    Returns:
        Iterable[AudioTranscript]: Stream of transcribed audio and metadata
    """
    num_chars_printed = 0
    transcript = None
    start_time = time.time()
    is_final = False
    for response in responses:
        if not is_final:
            if not response.results:
                if (response.speech_event_type.name == "END_OF_SINGLE_UTTERANCE"
                    or time.time() - start_time > deadline):
                    if transcript is None:
                        logger.info("No utterance detected for awhile..")
                    is_final = True
                    yield AudioTranscript(
                        transcript, is_final, deadline_exceeded=transcript is None
                    )
                else:
                    continue

            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            if not result.is_final:
                # Display interim results, but with a carriage return at the end of the
                # line, so subsequent lines will overwrite them.
                #
                # If the previous result was longer than this one, we need to print
                # some extra spaces to overwrite the previous result
                overwrite_chars = " " * (num_chars_printed - len(transcript))
                nlp_utils.display_live_transcription(transcript, overwrite_chars)
                num_chars_printed = len(transcript)

                # Eagerly return command if matches result
                if _is_supported_command(transcript, supported_commands):
                    logger.info("Detected a supported command! Exiting early.")
                    is_final = True

                yield AudioTranscript(transcript, is_final, overwrite_chars=overwrite_chars)

            else:
                logger.info(f"Current transcript: {transcript}")
                num_chars_printed = 0
                is_final = True
                yield AudioTranscript(transcript, is_final)
