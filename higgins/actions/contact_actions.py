from tinydb import TinyDB

from higgins.automation import contacts
from higgins.automation.contacts import Contact
from higgins.automation.email import email_utils


def clarify_contact_info(
    name: str,
    db: TinyDB,
    prompt_fn: str = input,
    loop_until_found: bool = True,
    prompt_for_alias: bool = False,
) -> Contact:
    possible_alias = None
    contact_info = None
    while contact_info is None:
        users = contacts.local.find_contact_in_database(db, name)
        if len(users) == 1:
            contact_info = Contact(**users[0])
        elif len(users) > 1:
            name = prompt_fn(f"Found {len(users)} contacts named {name}. Who do you mean by {name}?")
        elif loop_until_found:
            possible_alias = name
            name = prompt_fn(f"No contacts found for {name}. Who do you mean by {name}?")
            if email_utils.is_valid_email(name):
                return Contact(name=possible_alias, email=name)
        else:
            return None

    if prompt_for_alias and possible_alias is not None:
        add_alias = prompt_fn(
            f"Is '{possible_alias}' an alias for '{contact_info.name}'?"
        )
        if add_alias.strip().lower() in ["yes", "y"]:
            contact_info.alias = possible_alias.strip()
            # TODO: Update this to write to a contacts_aliases database
            contacts.local.update_contact(db, contact_info)

    return contact_info
