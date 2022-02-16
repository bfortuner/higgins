from higgins import const

from .basic_transcriber import BasicTranscriber  # noqa: F401
from .google_transcriber import GoogleTranscriber  # noqa: F401


def get_transcriber(name):
    if name == "basic":
        return BasicTranscriber()  # Also Google, but via SpeechRecognition
    elif name == "google":
        return GoogleTranscriber(
            supported_commands=const.SUPPORTED_COMMANDS, single_utterance=False
        )  # Performant, streaming listener
    raise Exception("Transcriber {name} not supported!")
