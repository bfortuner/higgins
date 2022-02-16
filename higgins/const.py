"""Shared constants."""

import os

USERNAME = "Brendan"
AGENT_NAME = "Higgins"

# Some files are platform specific like mac_automation.py.
# To avoid loading them, we only load files that contain actions
# which are determined by looking for file with this suffix.
ACTION_FILE_SUFFIX = "_actions.py"
INTENT_FILE_SUFFIX = "_intents.py"

OPENAI_CACHE_DIR = "openai_cache/"

DEBUG_MODE = bool(os.getenv("DEBUG_HIGGINS", False))

# Database
TINY_DB_PATH = "data/tinydb.json"
EPISODE_JSONL_PATH = "data/episodes.jsonl"

# Parameter names to exclude for serialization
AUTOMATION_PARAMS = ["browser", "desktop"]

# How long to wait before turning of the microphone (seconds)
SILENCE_TIMEOUT_SEC = 10

# How long to wait between GUI actions (e.g. debugging)
SPEED_LIMIT = float(os.getenv("SPEED_LIMIT", "0"))

# Wake words (Higgins was finetuned with Porcupine: https://picovoice.ai/platform/porcupine/)
WAKE_WORDS = ["jarvis"]
WAKE_WORD_PATHS = ["higgins__en_mac_2021-09-25-utc_v1_9_0.ppn"]  # "Higgins"

# Speech Synthesis
DEFAULT_VOICE_NAME = "en-GB-Wavenet-D"
JARVIS_PHRASES = [
    "Right!",
    "Very well!",
    "As you wish!",
    "Certainly.",
    "It shall be done!",
]
JARVIS_WAKE_PHRASES = [
    "Sir",
    "Sire",
    "M'lady",
    "M'lord",
    "Ready and waiting",
    # not as good...
    # "At your service",
    # "My queen",
    # "My lord",
    # "Your Grace",
    # "Your highness",
    # "Your excellency",
]
JARVIS_INTRO_SSML = f"""
<speak>
    <break time="200ms"/>
    Hello {USERNAME}, <break time="400ms"/>
    How can I help you?
</speak>
"""
JARVIS_WAKE_SSML = """
<speak>
    <break time="400ms"/>
    {wake_phrase} <break time="400ms"/>
</speak>
"""


def get_jarvis_wake_ssml():
    import random
    phrase = random.choices(JARVIS_WAKE_PHRASES)
    return JARVIS_WAKE_SSML.format(wake_phrase=phrase)
