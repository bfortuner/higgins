"""Module for shared NLP utilities.

Methods here should eventually be moved to specialist modules once common themes
can be identified across a number of utility methods. But this is a good starting place
for methods which don't have an obvious home yet.
"""
import hashlib
import os
import sys

from transformers import GPT2TokenizerFast


def get_num_tokens(text: str, tokenizer: GPT2TokenizerFast):
    """Return number of tokens in string."""
    return len(tokenizer(text)["input_ids"])


def get_tokenizer() -> GPT2TokenizerFast:
    # https://huggingface.co/transformers/main_classes/tokenizer.html#transformers.PreTrainedTokenizerFast
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    tokenizer = GPT2TokenizerFast.from_pretrained(
        "gpt2", cache_dir="transformers_cache/", local_files_only=True
    )
    return tokenizer


def normalize_text(text, method="naive"):
    if method == "naive":
        return normalize_text_naive(text)
    raise Exception(f"Method: '{method}' not supported!")


def normalize_text_naive(text):
    return text.lstrip().rstrip().lower()


def compute_levenshtein_distance(s1, s2):
    """Measure difference between 2 strings.

    https://en.wikipedia.org/wiki/Levenshtein_distance.

    TODO: Replace with open-source implementation
    """
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(
                    1 + min((distances[i1], distances[i1 + 1], distances_[-1]))
                )
        distances = distances_
    return distances[-1]


def match_text(
    target: str,
    text: str,
    fuzzy: bool = True,
    contains: bool = False,
    threshold: float = 2,
):
    target = normalize_text(target)
    text = normalize_text(text)
    if text == target:
        return True
    if fuzzy:
        print("Falling back to fuzzy matching")
        distance = compute_levenshtein_distance(target, text)
        if distance <= threshold:
            return True
    if contains:
        return text in target
    return False


def display_live_transcription(transcript, overwrite_chars):
    """Print interim results of live transcription to stdout.

    We include a carriage return at the end of the line, so subsequent lines will overwrite
    them. If the previous result was longer than this one, we need to print some extra
    spaces to overwrite the previous result
    """
    sys.stdout.write(transcript + overwrite_chars + "\r")
    sys.stdout.flush()


def hash_normalized_text(text, normalize=True):
    if normalize:
        text = normalize_text(text)
    text = text.encode("utf-8")
    return hashlib.sha256(text).hexdigest()


def trim_tokens(text: str, max_tokens: int, tokenizer: GPT2TokenizerFast = None):
    if tokenizer is None:
        tokenizer = get_tokenizer()
    tokens = tokenizer.tokenize(text)[:max_tokens]
    return tokenizer.convert_tokens_to_string(tokens)


if __name__ == "__main__":
    string = "Hello Brendan What is going on"
    tokenizer = get_tokenizer()
    print(trim_tokens(string, 3, tokenizer))
