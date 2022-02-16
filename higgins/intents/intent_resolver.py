
from typing import Dict, Tuple

from higgins.nlp.openai import intent_classifier

from higgins import const
from higgins.episode import Episode
from higgins.intents import IntentParser
from higgins.utils import class_registry


class IntentResolver:
    """Classify text and route to corresponding IntentParser."""


class RegexIntentResolver(IntentResolver):
    """Uses regular expressions to route to corresponding IntentParser."""

    def __init__(self, module_path: str = "higgins/intents"):
        self.intent_phrase_map = class_registry.load_class_phrase_map_from_modules(
            dir_name=module_path,
            file_suffix=const.INTENT_FILE_SUFFIX,
            class_type=IntentParser
        )

    def resolve(self, text: str) -> Tuple[IntentParser, Dict]:
        # Regex search for command prefix (e.g. send-msg, web-nav, open-website)
        intent_parsers = class_registry.find_matching_classes(
            phrase=text, phrase_map=self.intent_phrase_map
        )
        if len(intent_parsers) > 0:
            intent_class, intent_params = intent_parsers[0]  # We assume 1 matching intent parser
            return intent_class, intent_params["text"]
        else:
            return None, None


class OpenAIIntentResolver(IntentResolver):
    """Uses OpenAI to classify text and route to corresponding IntentParser."""

    def __init__(self, module_path: str = "higgins/intents"):
        self.intent_class_map = class_registry.load_classes_from_modules(
            dir_name=module_path,
            file_suffix=const.INTENT_FILE_SUFFIX,
            class_type=IntentParser
        )

    def resolve(self, text: str, episode: Episode = None) -> Tuple[IntentParser, Dict]:
        if episode is not None and episode.action_result is not None and episode.action_result.reply_handler_classname is not None:
            category = episode.action_result.reply_handler_classname
        else:
            category = intent_classifier.classify_intent_completion(text)
        if category == "Other":
            intent_class = None
        else:
            intent_class = class_registry.load_class_by_name(
                class_name=category, class_map=self.intent_class_map
            )
        return intent_class, text


if __name__ == "__main__":
    examples = [
        # Messaging
        ("send-msg", "ping Liam Fortuner and ask him when his flight lands"),
        ("send-msg", "email Dad and let him know I'm coming home for the holidays"),
        ("send-msg", "tell colin to grab me toilet paper at the store"),
        ("send-msg", "tell Mom I'm coming home for dinner"),
        ("send-msg", "ping Colin on slack"),
        # WebNav
        ("web-nav", "log in to my spotify account username david123"),
        ("web-nav", "search for apples and oranges on Instacart"),
        ("web-nav", "open etherscan"),
        ("web-nav", "search arxiv for resnet50 paper"),
        ("web-nav", "find airpods on ebay"),
        ("web-nav", "go to Best Sellers on Amazon.com"),
        ("web-nav", "go to circle ci and login with the username bfortuner"),
        ("web-nav", "find Jackie First on facebook"),
        ("web-nav", "open opensea io"),
        ("web-nav", "search for rainbows on google"),
        ("web-nav", "logout"),
        ("web-nav", "sign out"),
        ("web-nav", "login to Walmart.com"),
        # Other
        ("", "wondering what the air quality will be"),
        ("", "play Stan Getz on Spotify"),
        ("", "turn on the lights"),
        ("", "close all applications"),
        ("", "which app is using the most CPU?)")
    ]

    resolver = RegexIntentResolver()
    print("Regex intent resolver ------")
    for category, text in examples:
        combined = " ".join([category, text])
        intent_class, _ = resolver.resolve(combined)
        print(combined, intent_class)

    resolver = OpenAIIntentResolver()
    print("\nOpenAI intent resolver ------")
    for category, text in examples:
        intent_class, _ = resolver.resolve(text)
        print(text, intent_class)
