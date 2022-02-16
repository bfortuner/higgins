"""PromptKit utilities for building interactive CLI."""

import os
from pathlib import Path
import pprint
import sys

from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import (
    NestedCompleter,
)

from higgins.nlp import nlp_utils

pp = pprint.PrettyPrinter(indent=2)


def get_prompt_history(session, limit=10):
    # Ordered chronologically in desceneding order
    messages = []
    for text in session.history.load_history_strings():
        messages.append(text)
        if len(messages) >= limit:
            return messages
    return messages


def load_chat_history(chat_history_path):
    history = []
    if os.path.exists(chat_history_path):
        with open(chat_history_path) as f:
            context = f.readlines()
            return [line.strip() for line in context]
    return history


def save_chat_history(history, chat_history_path):
    Path(chat_history_path).parent.mkdir(parents=True, exist_ok=True)
    with open(chat_history_path, "w") as f:
        f.write("\n".join(history))


def add_text_to_chat_history(history, text, speaker):
    text = f"{speaker}: {text}"
    history.append(text)


def get_default_style():
    return Style.from_dict(
        {
            "": "#ffffff",  # default
            "user-prompt": "#884444",
            "bot-prompt": "#00aa00",
            "bot-text": "#A9A9A9",
        }
    )


def get_default_completer():
    return NestedCompleter.from_nested_dict(
        {
            "show": {"history": None, "commands": {"interface": {"brief"}}},
            "clear": {
                "history": None,
            },
            "exit": None,
            "quit": None,
        }
    )


def handle_prompt_commands(text, chat_history, chat_history_path=None):
    is_prompt_cmd = False
    text = nlp_utils.normalize_text(text)
    if text.lower().strip() in ["exit", "quit"]:
        if chat_history_path is not None:
            save_chat_history(chat_history, chat_history_path)
        sys.exit(0)
    elif text.lower().strip() == "show history":
        print("\n".join(chat_history[-10:]))
        is_prompt_cmd = True
    elif text.lower().strip() == "clear history":
        chat_history = []
        is_prompt_cmd = True
    return chat_history, is_prompt_cmd


def init_prompt_session(history_path=".prompt_history", style=None, completer=None):
    # https://python-prompt-toolkit.readthedocs.io/en/stable/pages/dialogs.html
    # Yes/No, or List of options, etc
    # https://python-prompt-toolkit.readthedocs.io/en/stable/pages/asking_for_input.html
    # Custom WordCompleter, FuzzyCompleter
    if style is None:
        style = get_default_style()
    if completer is None:
        completer = get_default_completer()

    kwargs = dict(
        auto_suggest=AutoSuggestFromHistory(),
        completer=completer,
        style=style,
    )
    if history_path:
        kwargs["history"] = FileHistory(history_path)

    return PromptSession(**kwargs)
