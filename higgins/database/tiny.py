from datetime import datetime
from typing import Any, Dict, List

import jsonlines
from tinydb import TinyDB, where

from higgins import const


class DateTimeSerializer():
    OBJ_CLASS = datetime  # The class this serializer handles

    def encode(self, obj):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')

    def decode(self, s):
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')


def load_database(db_path: str = const.TINY_DB_PATH) -> TinyDB:
    return TinyDB(db_path)


def truncate(table_name: str, db: TinyDB) -> None:
    table = db.table(table_name)
    table.truncate()


def insert(table_name: str, records: List[Dict], db: TinyDB) -> None:
    table = db.table(table_name)
    table.insert_multiple(records)


def query(table_name: str, field_name: str, field_value: Any, db: TinyDB) -> List[Dict]:
    table = db.table(table_name)
    records = table.search(where(field_name) == field_value)
    return records


def export_openai_jsonl(table_name: str, field_name: str, db: TinyDB, export_path: str):
    # Export in the openai format needed for search: https://beta.openai.com/docs/guides/search
    table = db.table(table_name)
    with jsonlines.open(export_path, 'w') as writer:
        for record in table:
            writer.write({"text": record[field_name], "metadata": ""})


def load_jsonl(jsonl_path: str, table_name: str, db: TinyDB):
    table = db.table(table_name)
    with jsonlines.open(jsonl_path) as reader:
        for record in reader:
            table.insert(record)


if __name__ == "__main__":
    db = load_database()
    print(db)
    table = db.table("episodes")
    print(table)
    chat_text = 'Brendan: Hello. Higgins: How can I help you?'
    insert(
        table_name="episodes",
        records=[
            {'context': {'active_window': 'Google Chrome', 'running_applications': []}, 'chat_text': chat_text, 'start_time': '2021-09-03T11:54:54'},
            {'context': {'active_window': 'App Store', 'running_applications': []}, 'chat_text': chat_text, 'start_time': '2021-09-03T11:54:54'}
        ],
        db=db
    )
    print(table.all())
    rows = query(table_name="episodes", field_name="chat_text", field_value=chat_text, db=db)
    print(rows)
    export_path = "data/episode_openai.jsonl"
    export_openai_jsonl(
        table_name="episodes",
        field_name="chat_text",
        db=db,
        export_path=export_path
    )

    from higgins.utils import jsonl_utils

    records = jsonl_utils.open_jsonl(export_path)
    print(records)

    truncate("episodes", db)
