from typing import Dict, List

from higgins.episode import Episode
from higgins.intents import IntentParser
from higgins.nlp.openai import messaging_completions, completion_utils


class Messaging(IntentParser):

    @classmethod
    def phrases(cls):
        return ["send-msg {text}"]

    def parse(cls, text: str, episode: Episode = None) -> List[Dict]:
        answer = messaging_completions.send_message_completion(text)
        actions = completion_utils.convert_string_to_action_chain(answer)
        return actions


if __name__ == "__main__":
    print(Messaging().parse("message mom I'm coming home tonight"))
