from pathlib import Path
from pprint import PrettyPrinter
import time
from typing import Dict, List, Optional

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools
from oauth2client.clientsecrets import InvalidClientSecretsError


pp = PrettyPrinter(indent=2)


class GoogleContacts:
    """
    The class which serves as the entrypoint for the Google People service API.

    https://developers.google.com/people
    https://contacts.google.com/u/1/

    Args:
        client_secret_file: The name of the user's client secret file.

    Attributes:
        client_secret_file (str): The name of the user's client secret file.
        service (googleapiclient.discovery.Resource): The People service object.

    """
    # https://developers.google.com/people/api/rest/v1/people/get
    _SCOPES = [
        'https://www.googleapis.com/auth/contacts',  # read/write
        'profile',  # Info about you
        'email',  # Your email address
    ]

    # Contact fields to return by default
    CONTACT_FIELDS = [
        "addresses",
        "ageRanges",
        "biographies",
        "birthdays",
        "calendarUrls",
        "clientData",
        "coverPhotos",
        "emailAddresses",
        "events",
        "externalIds",
        "genders",
        "imClients",
        "interests",
        "locales",
        "locations",
        "memberships",
        "metadata",
        "miscKeywords",
        "names",
        "nicknames",
        "occupations",
        "organizations",
        "phoneNumbers",
        "photos",
        "relations",
        "sipAddresses",
        "skills",
        "urls",
        "userDefined",
    ]

    # If you don't have a client secret file, follow the instructions at:
    # https://developers.google.com/gmail/api/quickstart/python
    # Make sure the client secret file is in the root directory of your app.

    def __init__(
        self,
        client_secret_file: str = 'client_secret.json',
        creds_file: str = 'google_tokens/google_people_token.json',
        _creds: Optional[client.Credentials] = None
    ) -> None:
        Path(client_secret_file).parent.mkdir(parents=True, exist_ok=True)
        Path(creds_file).parent.mkdir(parents=True, exist_ok=True)
        self.client_secret_file = client_secret_file
        self.creds_file = creds_file

        try:
            # The file google_people_token.json stores the user's access and refresh
            # tokens, and is created automatically when the authorization flow
            # completes for the first time.
            if _creds:
                self.creds = _creds
            else:
                store = file.Storage(self.creds_file)
                self.creds = store.get()

            if not self.creds or self.creds.invalid:

                # Will ask you to authenticate an account in your browser.
                flow = client.flow_from_clientsecrets(
                    self.client_secret_file, self._SCOPES
                )
                self.creds = tools.run_flow(flow, store)

            self.service = build(
                'people', 'v1', http=self.creds.authorize(Http()),
                cache_discovery=False
            )

        except InvalidClientSecretsError:
            raise FileNotFoundError(
                "Your 'client_secret.json' file is nonexistent. Make sure "
                "the file is in the root directory of your application. If "
                "you don't have a client secrets file, go to https://"
                "developers.google.com/gmail/api/quickstart/python, and "
                "follow the instructions listed there."
            )

    def people(self):
        return self.service.people()

    def list_contacts(
        self, fields: List[str] = CONTACT_FIELDS, limit: int = 10
    ) -> List[Dict]:
        # TODO: Support pagination over a larger number of contacts
        results = self.people().connections().list(
            resourceName='people/me',
            pageSize=limit,
            personFields=",".join(fields) if fields else None,
        ).execute()

        connections = results.get('connections', [])
        return connections

    def create_contact(self, profile: Dict):
        """Add new contact to Google Contacts.

        Example:
            self.people().createContact(body={
                "names": [
                    {
                        "givenName": "Samkit"
                    }
                ],
                "phoneNumbers": [
                    {
                        'value': "8600086024"
                    }
                ],
                "emailAddresses": [
                    {
                        'value': 'samkit5495@gmail.com'
                    }
                ]
            }).execute()
        """
        raise NotImplementedError

    def get_contact(
        self,
        resource_name: str = "people/me",
        fields: List[str] = CONTACT_FIELDS
    ) -> Dict:
        results = self.people().get(
            resourceName=resource_name,
            personFields=",".join(fields),
        ).execute()
        return results

    def search_contacts(
        self, query: str, fields: List[str] = CONTACT_FIELDS
    ) -> List[Dict]:
        """Search contacts by query.

        https://developers.google.com/people/api/rest/v1/people/searchContacts

        `query` matches contact [names, nickNames, emailAddresses, phoneNumbers, and organizations

        """

        # Warmup the cache
        results = self.people().searchContacts(
            query="",
            readMask=",".join(fields),
        ).execute()
        time.sleep(1)  # <-- possibly 5?

        results = self.people().searchContacts(
            query=query,
            readMask=",".join(fields),
        ).execute()
        return results


if __name__ == '__main__':
    client = GoogleContacts()
    contacts = client.list_contacts(limit=5)
    print(contacts)
    contacts = client.search_contacts("Bill Fortuner")
    pp.pprint(contacts)
    you = client.get_contact()
    print("ME")
    pp.pprint(you)
