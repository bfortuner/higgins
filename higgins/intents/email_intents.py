from higgins.nlp import nlp_utils
from typing import Dict, List

from higgins.episode import Episode
from higgins.intents import IntentParser
from higgins.nlp.openai import (
    completion_utils,
    email_completions
)


class SendEmail(IntentParser):

    @classmethod
    def phrases(cls):
        return ["send-email {text}"]

    def parse(cls, text: str, episode: Episode = None) -> List[Dict]:
        answer = email_completions.send_email_completion(text)
        actions = completion_utils.convert_string_to_action_chain(answer)
        return actions


class ComposeEmail(IntentParser):

    @classmethod
    def phrases(cls):
        return ["compose-email {text}"]

    def parse(cls, text: str, episode: Episode = None) -> List[Dict]:
        answer = email_completions.compose_email_completion(text)
        actions = completion_utils.convert_string_to_action_chain(answer)
        for action in actions:
            action["params"]["user_text"] = text
        return actions


class ComposeEmailReplyHandler(IntentParser):

    def parse(cls, text: str, episode: Episode) -> List[Dict]:
        text = nlp_utils.normalize_text(text)
        user_text = episode.action_result.data["user_text"]
        if text in ["try again", "regenerate", "regenerate email"]:
            print("Regenerating email..")
            answer = email_completions.compose_email_completion(user_text)
            actions = completion_utils.convert_string_to_action_chain(answer)
            for action in actions:
                action["params"]["user_text"] = user_text
        elif text in ["edit email", "edit", "refactor", "edit the email"]:
            print("Editing email..")
            actions = [
                {
                    "action": "EditEmail",
                    "params": {
                        "recipient": episode.action_result.data["recipient"],
                        "subject": episode.action_result.data["subject"],
                        "user_text": episode.action_result.data["user_text"],
                        "first_draft": episode.action_result.data["plain"],
                        "feedback": "???",
                    }
                }
            ]
        else:
            actions = [
                {
                    "action": "DisplayText",
                    "params": {
                        "text": "Sorry I don't understand.",
                        "data": episode.action_result.data,
                        "reply_handler_classname": "ComposeEmailReplyHandler",
                    }
                }
            ]
        return actions


class SearchEmail(IntentParser):

    @classmethod
    def phrases(cls):
        return ["search-email {text}"]

    def parse(cls, text: str, episode: Episode = None) -> List[Dict]:
        answer = email_completions.search_email_completion(text)
        actions = completion_utils.convert_string_to_action_chain(answer)
        return actions


class SearchEmailReplyHandler(IntentParser):

    def parse(cls, text: str, episode: Episode) -> List[Dict]:
        return [
            {
                "action": "AnswerEmailQuestion",
                "params": {
                    "data": episode.action_result.data, "question": text
                }
            }
        ]


if __name__ == "__main__":
    print(SendEmail().parse("email mom I'm coming home tonight"))
    print(SearchEmail().parse("get unread emails"))
    print(SearchEmail().parse("get emails sent by Yoon Manivanh"))
