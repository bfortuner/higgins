from typing import Dict, List

from higgins.episode import Episode


class IntentParser:
    """Base class for all IntentParsers.

    IntentParsers know how to:
    - Parse text into a sequence of actions
    - Prompt the user with clarifying questions to finalize parameters???
    """

    @classmethod
    def phrases(cls) -> List[str]:
        """List of phrases which trigger this IntentParser.

        Right now, these are hard-coded (e.g. send-msg, web-nav), but in the
        future we can incorporate a classification module which takes user
        text and routes it to the corresponding intent parser.
        """
        return []

    @property
    def name(self):
        return type(self).__name__

    def parse(self, text: str, episode: Episode = None) -> List[Dict]:
        """Given text, parse intent, parameters, and sub-actions."""
        raise NotImplementedError("Needs to be implemented by derived class")
