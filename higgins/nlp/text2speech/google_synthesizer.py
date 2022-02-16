"""Convert text to speech using Google Cloud APIs."""

import os

from google.cloud import texttospeech
from google.cloud.texttospeech import AudioEncoding, SsmlVoiceGender

from higgins.nlp import nlp_utils
from higgins.nlp.text2speech import audio_utils


def convert_text_to_speech(
    text=None,
    ssml=None,
    voice_name=None,  # If set, will override the following 2 params
    voice_gender=SsmlVoiceGender.FEMALE,
    language_code="en-US",
    encoding=AudioEncoding.LINEAR16,
):
    """Synthesizes speech from the input string of text or ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/

        LINEAR16 = Wav files (uncompressed)
        MP3 (compressed, for distribution)
    """
    assert text is not None or ssml is not None, "must provide text or ssml"

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text, ssml=ssml)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, ssml_gender=voice_gender, name=voice_name
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=encoding,
        speaking_rate=1.05,
        pitch=0,  # -20,20
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The `response.audio_content` is binary.
    return response.audio_content


def load_or_convert_text_to_speech(
    text=None,
    ssml=None,
    voice_name=None,  # If set, will override the following 2 params
    voice_gender=SsmlVoiceGender.FEMALE,
    language_code="en-US",
    encoding=AudioEncoding.LINEAR16,  # wav
    cache_dir="audio_cache/",
):
    assert text is not None or ssml is not None, "must provide text or ssml"
    text_hash = nlp_utils.hash_normalized_text(f"{text or ssml}__{voice_name}")
    fpath = os.path.join(cache_dir, f"{text_hash}.wav")
    if os.path.exists(fpath):
        print(f"Found existing audio file for '{text or ssml}'")
        audio_bytes = audio_utils.load_audio_from_file(fpath)
    else:
        print("Converting text to speech")
        audio_bytes = convert_text_to_speech(
            text=text,
            ssml=ssml,
            voice_name=voice_name,
            voice_gender=voice_gender,
            language_code=language_code,
            encoding=encoding
        )
        print(f"No existing audio file found. Saving audio file {fpath}")
        audio_utils.save_audio_to_file(fpath, audio_bytes, tags={
            "text": text or ssml, "hash": text_hash}
        )
    return audio_bytes
