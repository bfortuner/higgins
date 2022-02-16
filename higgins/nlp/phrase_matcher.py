import re
from typing import Tuple


class PhraseMatcher:
    def __init__(self, phrase, conjunctive=False):
        super()

        self._phrase = phrase
        self._matcher = self._convert_to_regex(phrase)
        self._conjunctive = conjunctive

    def match(self, cmd) -> Tuple[bool, dict]:
        """Returns a tuple of (success, matched_params_dict)"""
        m = self._matcher.match(cmd)
        if m is None: return (False, None)

        return (True, m.groupdict())

    def is_conjunctive(self):
        return self._conjunctive

    def _convert_to_regex(self, phrase):
        # TODO(hari): Support and handle different types
        # of variables here. For now everything is assumed
        # as a string.
        regexp = phrase.replace('{', '(?P<').replace('}', '>.+)')
        # logging.info(phrase)
        # logging.info(regexp)
        return re.compile(regexp)
