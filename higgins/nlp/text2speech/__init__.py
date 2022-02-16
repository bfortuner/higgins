from . import google_synthesizer  # noqa: F401
from . import audio_utils  # noqa: F401

from higgins.const import DEFAULT_VOICE_NAME


def speak_text(text=None, ssml=None, enable=True, voice=DEFAULT_VOICE_NAME):
    if enable:
        audio_bytes = google_synthesizer.load_or_convert_text_to_speech(
            text=text, ssml=ssml, voice_name=voice
        )
        audio_utils.play_audio_bytes(audio_bytes)
