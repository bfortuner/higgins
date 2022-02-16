"""Utilities for interacting with keyboard"""

from typing import List

import pyautogui


class Keyboard():
    def type(self, text: str):
        """Type the text in the active window"""
        pyautogui.typewrite(text)

    def press_key(self, key: str):
        return self.press_keys(keys=[key])

    def press_keys(self, keys: List[str]):
        """Press keys in sequence."""
        pyautogui.typewrite(keys)

    def shortcut(self, keys: List[str]):
        """Simulate pressing specified keyboard shortcut (all pressed together)
        on the currently active window.

        `keys` are specified as a list of keys including modifiers like ctrl, alt, etc.,
        """
        pyautogui.hotkey(*keys)
