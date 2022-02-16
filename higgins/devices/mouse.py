"""Utilities for interacting with mouse"""

import pyautogui


class Mouse():
    def current_position(self) -> list:
        """Return the `x` and `y` coords of the mouse"""
        return pyautogui.position()

    def move_to(self, x, y) -> None:
        """Move mouse to specified `x` and `y` coordinates"""
        pyautogui.moveTo(x, y)

    def click(self, button='left'):
        """Click the specified button for the specified number of times.

        Valid options for button include `left`, `right` and `middle`."""
        assert button in ("left", "right", "middle", "double", "triple")
        if button == "double":
            pyautogui.click(button="left", clicks=2)
        elif button == "triple":
            pyautogui.click(button="left", clicks=3)
        else:
            pyautogui.click(button=button, clicks=1)

    def scroll(self, direction: str, amount: int = 10):
        """Scroll mouse for specified amount in direction.

        NOTE: The location of the mouse pointer determines which
        window is scrolled.

        Args:
            amount: positive integer indicating magnitude of scroll
            direction: "up", "down", "left", "right"
        """
        if direction == "left":
            pyautogui.hscroll(-amount)
        elif direction == "right":
            pyautogui.hscroll(amount)
        elif direction == "up":
            pyautogui.scroll(amount)
        elif direction == "down":
            pyautogui.scroll(-amount)
        else:
            raise Exception(f"Scroll direction {direction} not supported.")
