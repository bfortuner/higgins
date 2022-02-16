"""Stores context and chat history for a single exchange."""

from datetime import datetime
from typing import List
import uuid

from tinydb.database import TinyDB

from higgins import const
from higgins.actions import ActionResult
from higgins.context import Context
from higgins.database import tiny
from dataclasses import asdict, dataclass, field

EPISODE_TABLE_NAME = "episodes"


@dataclass
class Episode:
    chat_text: str
    context: Context = None
    action_result: ActionResult = None
    end_time: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    episode_id: str = field(default_factory=lambda: str(uuid.uuid1()))


def save_episode(episode: Episode, db: TinyDB, dump_to_jsonl: bool = True):
    records = tiny.query(EPISODE_TABLE_NAME, "chat_text", episode.chat_text, db)
    if len(records) > 0:  # Avoid duplicates, like intros, wakeup words
        pass
    else:
        tiny.insert(EPISODE_TABLE_NAME, records=[asdict(episode)], db=db)

    if dump_to_jsonl:
        tiny.export_openai_jsonl(
            table_name=EPISODE_TABLE_NAME,
            field_name="chat_text",
            db=db,
            export_path=const.EPISODE_JSONL_PATH,
        )


if __name__ == "__main__":
    context = Context(active_window="Google Chrome")
    episode = Episode(context=context, chat_text="Brendan: Hello. Higgins: How can I help you?")
    print(episode)
    print(asdict(episode))

    chat_history = [
        "Brendan: Message Leeman 'Yo man' on WhatsApp",
        "Higgins: No contacts found for Leeman. Who do you mean?",
        "Brendan: Bill Jack",
        "Higgins: Is 'Leeman' an alias for 'Bill Jack'?",
        "Brendan: Yes",
    ]
    db = tiny.load_database()
    save_episode(chat_history, db)
