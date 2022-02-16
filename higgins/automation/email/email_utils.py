from datetime import datetime
import email
import hashlib
from html2text import HTML2Text
import json
import mistletoe
from pathlib import Path
import re
import sys
import time
from typing import Dict, List, Tuple, Union

from bs4 import BeautifulSoup

from higgins.automation.email import email_model
from higgins.nlp import html2plain


def dateconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


def is_valid_email(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex, email):
        return True
    return False


def get_email_list_preview(emails: List[Dict], limit: int = 50) -> str:
    display = []
    for idx, email in enumerate(emails):
        display.append(f"[{idx}] {email['sender']} subject: {email['subject']}")
    text = f"Found {len(emails)} emails.\n"
    if len(emails) > limit:
        text += f"Displaying {limit} out of {len(emails)} emails:\n"
    text += "\n".join(display[:limit])
    return text


def get_email_preview(
    email: Dict, max_lines=sys.maxsize, show_body: bool = True
) -> str:
    lines = []
    if email.get("recipient"):
        lines.append(f"\nTo: {email['recipient']}")
    if email.get("sender"):
        lines.append(f"\nFrom: {email['sender']}")
    if email.get("date"):
        lines.append(f"\nDate: {email['date']}")
    lines.append(f"\nSubject: {email['subject']}\n")

    # If the user asks to preview the email, attempt to show the plain version
    # Otherwise fallback to the HTML (which may not be available...)
    if show_body:
        if bool(email["plain"]):
            body_lines = email["plain"].split("\n")[:max_lines]
            lines += [f"\n{line}" for line in body_lines]
        else:
            print("text/plain not found. Falling back to text/html")
            lines += f"\n{email.get('html', '')}"
    else:
        lines.append(f"Preview: {email.get('preview')}")

    if email.get("email_id"):
        lines.append(f"\nEmail_id: {email['email_id']}")
    if email.get("google_id"):
        lines.append(f"\nGoogle_id: {email['google_id']}")

    preview = "".join(lines)
    preview += "\n\nThanks,\nBrendan"
    return preview


def get_email_body_extended(email: Dict, max_lines=sys.maxsize) -> str:
    """Return body with subject, from and date fields prepended."""
    lines = []
    # if email.get("recipient"):
    #     lines.append(f"\nTo: {email['recipient']}")
    if email.get("sender"):
        lines.append(f"\nFrom: {email['sender']}")
    if email.get("date"):
        lines.append(f"\nDate: {email['date']}")
    lines.append(f"\nSubject: {email['subject']}\n")

    if bool(email["plain"]):
        body_lines = email["plain"].split("\n")[:max_lines]
        lines += [f"\n{line}" for line in body_lines]
    else:
        print("text/plain not found. Falling back to text/html")
        lines += f"\n{email.get('html', '')}"

    return "".join(lines)


def clean_email_body(body: str):
    # https://pypi.org/project/clean-text/ ??
    body = body.replace("\r", "")
    body = re.sub(r"\n\s*\n", "\n\n", body)
    body = body.strip("\n")
    return body


def remove_whitespace(body: str):
    # body = " ".join(body.split())
    body = re.sub(r"\s+", " ", body)
    body = body.strip().strip("\n")
    return body


def parse_html(html):
    # This one preserves lists and newlines better, but doesn't handle
    # tags like <string style="margin: 5px">
    elem = BeautifulSoup(html, features="html.parser")
    text = ""
    for e in elem.descendants:
        if isinstance(e, str):
            text += e.strip()
        elif e.name in ["br", "p", "h1", "h2", "h3", "h4", "tr", "th"]:
            text += "\n"
        elif e.name == "li":
            text += "\n- "
    return text


def parse_html_v2(html):
    soup = BeautifulSoup(html)
    plain = soup.get_text("\n")
    return plain


def parse_html_v3(html):
    soup = BeautifulSoup(html)
    plain = [text for text in soup.stripped_strings]
    return "\n".join(plain)


def html2md(html):
    parser = HTML2Text()
    parser.ignore_images = True
    parser.ignore_anchors = True
    parser.body_width = 0
    md = parser.handle(html)
    return md


def html2plain_fn(html):
    # HTML to Markdown
    md = html2md(html)
    # Normalise custom lists
    md = re.sub(r"(^|\n) ? ? ?\\?[•·–-—-*]( \w)", r"\1  *\2", md)
    # Convert back into HTML
    html_simple = mistletoe.markdown(md)
    # Convert to plain text
    soup = BeautifulSoup(html_simple)
    text = soup.getText()
    # Strip off table formatting
    text = re.sub(r"(^|\n)\|\s*", r"\1", text)
    # Strip off extra emphasis
    text = re.sub(r"\*\*", "", text)
    # Remove trailing whitespace and leading newlines
    text = re.sub(r" *$", "", text)
    text = re.sub(r"\n\n+", r"\n\n", text)
    text = re.sub(r"^\n+", "", text)
    return text


def parse_html_v4(html):
    # Preserves some structure by using markdown as intermediary representation
    # https://skeptric.com/html-to-text/
    return html2plain_fn(html)


def parse_email_html(html: str) -> dict:
    # Minify HTML, Simplify HTML, Convert To Text
    return html2plain.parse_html(html)


def get_body_stats(body):
    lines = body.split("\n")
    words = body.replace("\n", " ").split()
    return {
        "lines": len(lines),
        "words": len(words),
        "chars": len(body),
    }


def save_email(
    email: Dict,
    dataset_dir: str = "data/emails",
    labels: Dict = None,
    include_elastic: bool = False,
) -> str:
    # Google has a unique identifier, but for now..
    email_id = hash_email(email)
    _ = save_email_to_dir(email_id, email, dataset_dir, labels)
    if include_elastic:
        _ = save_email_to_elastic(email)
    return email_id


def save_email_to_elastic(email: Dict):
    email = email_model.from_gmail_dict(email)
    email.save()
    email = email.get(id=email["google_id"])
    return email


def normalize_email_address(email_in):
    parsed = email.utils.parseaddr(email_in)
    return parsed


def load_email(
    email_id: str = None, email_dir: str = None, dataset_dir: str = "data/emails"
) -> Dict:
    if email_dir is None:
        assert email_id is not None, "must provide email_id or email_dir"
        email_dir = Path(dataset_dir, email_id)
    email = json.load(open(Path(email_dir, "metadata.json")))
    email.update({"plain": None, "html": None, "model_labels": None})
    plain_path = Path(email_dir, "body.plain")
    if plain_path.exists():
        with open(plain_path) as f:
            email["plain"] = f.read()

    html_path = Path(email_dir, "body.html")
    if html_path.exists():
        with open(html_path) as f:
            email["html"] = f.read()

    labels_path = Path(email_dir, "model_labels.json")
    if labels_path.exists():
        email["model_labels"] = json.load(open(labels_path))

    return email


def search_local_emails(
    categories: List[str], match_all: bool = True, dataset_dir: str = "data/emails"
) -> List[Dict]:
    """Search local database of emails.

    Args:
        categories: List of categories to include in query (e.g. flights, personal)
        match_all: If true, all categories in `categories` must be present in emails.
            If false, a match will occur if any category is present.
    """
    email_dirs = [f for f in Path(dataset_dir).iterdir() if f.is_dir()]
    emails = []
    for email_dir in email_dirs:
        email = load_email(email_dir=email_dir, dataset_dir=dataset_dir)
        matches = set(categories) & set(email["model_labels"]["categories"])
        if match_all:
            if len(matches) == len(categories):  # match all
                emails.append(email)
        elif len(matches) > 0:  # match any
            emails.append(email)
    print(f"search returned {len(emails)}")
    return emails


def save_email_to_dir(
    email_id: str, email: Dict, dataset_dir: str, labels: Dict = None
) -> str:
    """Save email body and metadata to email dataset directory.

    Args:
        email: dictionary of email body and metadata (from google)
        dataset_dir: root directory of email dataset
        labels: Optional dictionary of labels for training models

    Returns
        Email directory path

    Steps:
    1. Hash the parameters into a unique string (perhaps add salt)
        hash = subject, sender, recipient, date, body, cc, bcc?
    2. Create a directory named `{email_dir}/{email_hash}`
    3. Save the email data to the directory as follows:
        body.plain
        body.html  <-- optional
        metadata.json
            sender: str  <--ensure valid email? Include name?
            recipient: str  <--ensure valid email? Include name?
            subject: str
            labels: List[str]
            google_id: str
        edits.txt  <-- optional
            FEEDBACK
                blah blah blah
            REVISED_EMAIL
                blah blah blah
        labels.json <-- optional
            summary: str
            categories: List[str]
            question_answer: Tuple[str, str]
    """
    email_dir = Path(dataset_dir, email_id)
    email_dir.mkdir(parents=True, exist_ok=True)  # danger, may overwrite

    print(f"Saving email to: {email_dir}")

    exclude_fields = ["plain", "html", "attachments"]
    metadata = {k: v for k, v in email.items() if k not in exclude_fields}
    metadata["email_id"] = email_id
    # metadata["date"] = metadata["date"].isoformat()

    json.dump(
        metadata,
        open(Path(email_dir, "metadata.json"), "w"),
        indent=2,
        default=dateconverter,
    )

    if bool(email.get("plain")):
        with open(Path(email_dir, "body.plain"), "w") as f:
            f.write(email["plain"])

    if bool(email.get("html")):
        with open(Path(email_dir, "body.html"), "w") as f:
            f.write(email["html"])

    if bool(email.get("markdown")):
        with open(Path(email_dir, "body.md"), "w") as f:
            f.write(email["markdown"])

    if labels is not None:
        json.dump(labels, open(Path(email_dir, "model_labels.json"), "w"), indent=2)

    return email_dir


def format_newer_than_param(param: Union[Tuple[int, str], str]) -> Tuple:
    """Convert newer_than or after_than parameter into correct format.

    Args:
        param: Either tuple (1, day) or strings "1 day" or "1,day"

    Returns:
        Tuple of field_name, field_value
    """
    field_name = "newer_than"
    if isinstance(param, str):
        if "," in param:
            num, unit = param.replace(" ", "").split(",")
        else:
            num, unit = param.split()
        num = int(num)

    if unit[-1] == "s":
        unit = unit[:-1]

    if unit not in ["hour", "day", "month", "week", "year"]:
        raise Exception(f"`newer_than` unit '{unit}' not supported.")

    if unit == "week":
        field_value = num * 7, "day"
    elif unit == "hour":
        field_name = "after"
        field_value = int(time.time()) - num * 3600
    else:
        field_value = (num, unit)

    return field_name, field_value


def hash_email(email: Dict) -> str:
    hash_input = ""
    hash_input += f"{email['sender']}"
    hash_input += f"{email['recipient']}"
    hash_input += f"{email['subject']}"
    hash_input += f"{email['plain']}"
    hash_input = hash_input.encode("utf-8")
    return hashlib.sha256(hash_input).hexdigest()


if __name__ == "__main__":
    # email_dict = load_email(
    #     email_dir="data/emails/3f50ce2a8e1fd4a1120dd5b67dbe2799ec2c838d09d32b8ec1c15ab74755cd70"
    # )
    # email_model.Email.init()
    # es_email = save_email_to_elastic(email_dict)
    # print(es_email)
    # import pdb

    # pdb.set_trace()
    normalize_email_address("Colin Fortuner <colin@gather.town>")

    emails = search_local_emails([])
    print(len(emails))
