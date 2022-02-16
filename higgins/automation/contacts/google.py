"""Load contacts from Google Cloud People API.

Setup instructions are similar to the Gmail ones here: https://github.com/jeremyephron/simplegmail

1. Create/reuse a google cloud project
2. Enable the People API https://developers.google.com/workspace/guides/create-project?authuser=1#enable-api
3. Enable OAuth sign-in
4. Create credentials and download the client_secret.json file into repo root
"""

import os
import re
from typing import Dict, List

import pandas as pd
from tinydb import TinyDB, Query

from higgins.automation.contacts import Contact
from higgins.automation.google.people import GoogleContacts
from higgins.database import tiny


TABLE_NAME = "google_contacts"
CONTACTS_CSV_PATH = "data/google/contacts.csv"


def load_contacts_from_csv(csv_path: str = CONTACTS_CSV_PATH) -> List[Dict]:
    """Load google contacts from exported .csv file

    NOTE: It turns out this is actually a worse approach. Better to use the API.

    Export your Google Contacts as csv (https://contacts.google.com/u/1/)
    to the `csv_path`.

    In the future, we may be able to sync contacts periodically.
    https://developers.google.com/people/v1/contacts#list_the_users_contacts_that_have_changed
    """
    if not os.path.exists(csv_path):
        raise Exception(
            "Google contacts file {csv_path} does not exist. Export your contacts at https://contacts.google.com/u/1/"
        )
    df = pd.read_csv(csv_path)
    return df.to_dict(orient="records")


def load_contacts_from_api(limit: int = 2000) -> List[Dict]:
    """Load google contacts from Google People API.

    TODO: Paginate to download more than 2000 contacts.

    Requirements:
        If you don't have a client secret file, follow the instructions at:
        https://developers.google.com/gmail/api/quickstart/python
        Make sure the client secret file is in the root directory of your app.

    Args:
        limit: maximum number of contacts to return
    """
    client = GoogleContacts()
    contacts = client.list_contacts(limit=limit)
    return contacts


def load_contacts_from_table(table_name: str = TABLE_NAME) -> None:
    """Load google contacts from database."""
    db = tiny.load_database()
    table = db.table(table_name)
    return table.all()


def insert_contacts_into_db(contacts: List[Dict], table_name: str = TABLE_NAME) -> None:
    db = tiny.load_database()
    tiny.insert(table_name, contacts, db)


def init_google_contacts_table(
    csv_path: str = None, table_name: str = TABLE_NAME
) -> None:
    db = tiny.load_database()
    tiny.truncate(table_name, db)

    if csv_path is not None:
        contacts = load_contacts_from_csv()
    else:
        contacts = load_contacts_from_api()

    tiny.insert(table_name, contacts, db)


def find_contact_in_database(db: TinyDB, name: str) -> List[Dict]:
    """Lookup contact in local Google contacts table.

{ 'birthdays': [ { 'date': {'day': 27, 'month': 3},                                                                                                                           
                     'metadata': { 'primary': True,                                                                                                                             
                                   'source': { 'id': '540c39998b152984',                                                                                                        
                                               'type': 'CONTACT'}},                                                                                                             
                     'text': 'March 27'}],                                                                                                                                      
    'clientData': [ { 'key': 'GCon',                                                                                                                                            
                      'metadata': { 'primary': True,                                                                                                                            
                                    'source': { 'id': '540c39998b152984',                                                                                                       
                                                'type': 'CONTACT'}},                                                                                                            
                      'value': '<cc>0</cc>'}],                                                                                                                                  
    'coverPhotos': [ { 'default': True,                                                                                                                                         
                       'metadata': { 'primary': True,                                                                                                                           
                                     'source': { 'id': '110237801405153258330',                                                                                                 
                                                 'type': 'PROFILE'}},                                                                                                           
                       'url': 'https://lh3.googleusercontent.com/c5dqxl-2uHZ82ah9p7yxrVF1ZssrJNSV_15Nu0TUZwzCWqmtoLxCUJgEzLGtxsrJ6-v6R6rKU_-FYm881TTiMCJ_=s1600'}], 
    'emailAddresses': [ { 'metadata': { 'primary': True,                                                                                                                        
                                        'source': { 'id': '540c39998b152984',                                                                                                   
                                                    'type': 'CONTACT'}},                                                                                                        
                          'value': 'liam.fortuner@gmail.com'}],                                                                                                                 
    'etag': '%EiMBAgMFBgcICQoLDA0ODxATFBUWGSEiIyQlJicuNDU3PT4/QBoEAQIFByIMUjc1aGhXT1ZFc2c9',                                                                                    
    'memberships': [ { 'contactGroupMembership': { 'contactGroupId': '40ef4cf3093a233e',                                                                                        
                                                   'contactGroupResourceName': 'contactGroups/40ef4cf3093a233e'},                                                               
                       'metadata': { 'source': { 'id': '540c39998b152984',                                                                                                      
                                                 'type': 'CONTACT'}}},                                                                                                          
                     { 'contactGroupMembership': { 'contactGroupId': '500f6948082602c3',                                                                                        
                                                   'contactGroupResourceName': 'contactGroups/500f6948082602c3'},                                                               
                       'metadata': { 'source': { 'id': '540c39998b152984',                                                                                                      
                                                 'type': 'CONTACT'}}},                                                                                                          
                     { 'contactGroupMembership': { 'contactGroupId': 'myContacts',                                                                                              
                                                   'contactGroupResourceName': 'contactGroups/myContacts'},
                       'metadata': { 'source': { 'id': '540c39998b152984',
                                                 'type': 'CONTACT'}}},
                     { 'contactGroupMembership': { 'contactGroupId': 'starred',                                                                                                 
                                                   'contactGroupResourceName': 'contactGroups/starred'},
                       'metadata': { 'source': { 'id': '540c39998b152984',
                                                 'type': 'CONTACT'}}}],
    'metadata': { 'objectType': 'PERSON',                                                                                                                                       
                  'sources': [ { 'etag': '#R75hhWOVEsg=',
                                 'id': '540c39998b152984',
                                 'type': 'CONTACT',                     
                                 'updateTime': '2021-09-05T23:26:15.840821Z'},
                               { 'etag': '#zq6HT/mH+2o=',
                                 'id': '110237801405153258330',
                                 'profileMetadata': { 'objectType': 'PERSON',
                                                      'userTypes': [ 'GOOGLE_USER']},
                                 'type': 'PROFILE',                                                                                                                             
                                 'updateTime': '2021-04-14T02:27:02.803Z'}]},
    'names': [ { 'displayName': 'Liam Fortuner',
                 'displayNameLastFirst': 'Fortuner, Liam',
                 'familyName': 'Fortuner',
                 'givenName': 'Liam',
                 'metadata': { 'primary': True,
                               'source': { 'id': '540c39998b152984',
                                           'type': 'CONTACT'}},
                 'unstructuredName': 'Liam Fortuner'}],
    'nicknames': [ { 'metadata': { 'primary': True,
                                   'source': { 'id': '540c39998b152984',
                                               'type': 'CONTACT'}},
                     'value': 'Leeman'}],
    'phoneNumbers': [ { 'canonicalForm': '+18604598423',
                        'formattedType': 'Mobile',
                        'metadata': { 'primary': True,
                                      'source': { 'id': '540c39998b152984',
                                                  'type': 'CONTACT'},
                                      'sourcePrimary': True},
                        'type': 'mobile',
                        'value': '(860) 459-8423'}],
    'photos': [ { 'metadata': { 'primary': True,
                                'source': { 'id': '110237801405153258330',
                                            'type': 'PROFILE'}},
                  'url': 'https://lh3.googleusercontent.com/a-/AOh14Ghlb1bWk90eIFNarqckL2lw-V5FBnL7RcLxYKQ0=s100'},
                { 'default': True,
                  'metadata': { 'source': { 'id': '540c39998b152984',
                                            'type': 'CONTACT'}},
                  'url': 'https://lh3.googleusercontent.com/cm/ABXenNlFt81SLZMcmJRi3BMgTmp9M7nKWDzAnlQWz05FuPF1Hd1mpDg9PGbccrt1m3kR=s100'}],
    'relations': [ { 'formattedType': 'Brother',
                     'metadata': { 'primary': True,
                                   'source': { 'id': '540c39998b152984',
                                               'type': 'CONTACT'}},
                     'person': 'Brother',
                     'type': 'brother'}],
    'resourceName': 'people/c6056278930532673924'}]
    """
    table = db.table(TABLE_NAME)
    # print(f"Num Contacts: {len(table)}")

    User = Query()
    Name = Query()

    # Allow nicknames / aliases to take precedent 
    rows = table.search(
        User.nicknames.any(
            Name.value.matches(name, flags=re.IGNORECASE)
        )
    )
    if len(rows) != 1:
        rows = table.search(
            User.names.any(
                Name.displayName.matches(name, flags=re.IGNORECASE)
            ) |
            User.names.any(
                Name.unstructuredName.matches(name, flags=re.IGNORECASE)
            ) |
            User.relations.any(
                Name.type.matches(name, flags=re.IGNORECASE)
            ) |
            User.relations.any(
                Name.person.matches(name, flags=re.IGNORECASE)
            ) |
            User.nicknames.any(
                Name.value.matches(name, flags=re.IGNORECASE)
            )
        )
    # print(f"Found {len(rows)} matching contacts for name `{name}`")

    contacts = []
    for row in rows:
        contacts.append(convert_google_contact_to_contact(row))
    return contacts


def convert_google_contact_to_contact(row: Dict) -> Contact:
    def is_primary(field):
        return field["metadata"].get("primary")

    name = list(filter(is_primary, row.get("names", [])))
    phone = list(filter(is_primary, row.get("phoneNumbers", [])))
    email = list(filter(is_primary, row.get("emailAddresses", [])))
    alias = list(filter(is_primary, row.get("nicknames", [])))

    return dict(
        name=name[0]["displayName"],
        alias=alias[0]["value"] if alias else None,
        email=email[0]["value"] if email else None,
        phone=phone[0]["canonicalForm"] if phone else None,
        contact_id=row["resourceName"],
    )


if __name__ == "__main__":
    # python -m higgins.automation.contacts.google
    # csv_contacts = load_contacts_from_csv()
    # print(f"Num csv contacts: {len(csv_contacts)}")
    init_google_contacts_table()
    db_contacts = load_contacts_from_table()
    print(f"Num contacts in db: {len(db_contacts)}")
    from pprint import PrettyPrinter
    pp = PrettyPrinter(indent=2)
    # pp.pprint(db_contacts[:2])

    # name = "Leeman"
    # contacts = find_contact_in_database(db=tiny.load_database(), name=name)
    # pp.pprint(contacts)
    # print(f"Found {len(contacts)} matching contacts for name `{name}`")
