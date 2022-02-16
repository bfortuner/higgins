import re
from typing import Dict, List
from dataclasses import asdict

from tinydb import TinyDB, Query, where

from higgins.database import tiny
from higgins.automation.contacts import Contact


CONTACTS_TABLE_NAME = "contacts"


def add_contact(db: TinyDB, contact: Contact) -> None:
    record = asdict(contact)
    tiny.insert(CONTACTS_TABLE_NAME, [record], db)


def update_contact(db: TinyDB, contact: Contact) -> None:
    table = db.table(CONTACTS_TABLE_NAME)
    ids = table.update(
        fields=asdict(contact),
        cond=where("contact_id") == contact.contact_id
    )
    if len(ids) == 0:
        raise Exception(
            "No matching contact found to update for id: {contact.contact_id}"
        )


def find_contact(db: TinyDB, name: str) -> List[Dict]:
    rows = []
    if db is not None:
        rows = find_contact_in_database(db, name)
    return rows


def find_contact_in_database(db: TinyDB, name: str) -> List[Dict]:
    User = Query()
    table = db.table(CONTACTS_TABLE_NAME)
    rows = table.search(
        (User.name.matches(name, flags=re.IGNORECASE) |
            User.alias.matches(name, flags=re.IGNORECASE))
    )
    # print(f"Found {len(rows)} matching rows for {name}")
    return rows


def find_contact_semantic_search():
    """Run semantic search over raw documents to find contact."""
    pass


def init_local_contacts_table():
    db = tiny.load_database()
    tiny.truncate(CONTACTS_TABLE_NAME, db=db)
    contacts = [
        Contact(name="Colin Fortuner", alias="Colin", phone="8604598426"),
        Contact(name="Erin Fortuner", alias="Mom", phone="8604598425"),
        Contact(name="Bill Fortuner", email="chgas1@gmail.com"),
        Contact(name="Bill Jack"),
        Contact(name="Jackie First", email="jackie123@gmail.com", phone="860-459-8424"),
    ]
    tiny.insert(CONTACTS_TABLE_NAME, [asdict(c) for c in contacts], db=db)


if __name__ == "__main__":
    init_local_contacts_table()

    db = tiny.load_database("data/tinydb.json")
    assert len(find_contact(db, "Colin Fortuner")) > 0

    # print(db.table(CONTACTS_TABLE_NAME).all())
    # print(tiny.query(CONTACTS_TABLE_NAME, "name", "Erin Fortuner", db=db))

    # assert len(find_contact_in_database(db, "Bill Fortuner")) == 1
    # assert len(find_contact_in_database(db, "Brendan")) == 0
    # assert len(find_contact_in_database(db, "Erin")) == 1
    # assert len(find_contact_in_database(db, "Mom")) == 1
    # assert len(find_contact_in_database(db, "Bill")) == 2

    # contact_dict = find_contact_in_database(db, "Bill Jack")[0]
    # contact = Contact(**contact_dict)
    # contact.alias = "Fred"
    # update_contact(db, contact)

    # contact = find_contact_in_database(db, "Bill Jack")
    # print(contact)

    # contact = find_contact(db, "Bill Jack")
    # print(contact)

    # tiny.truncate(CONTACTS_TABLE_NAME, db=db)
