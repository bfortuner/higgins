from datetime import datetime
from typing import Dict

from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, connections


connections.create_connection(hosts=["localhost"], timeout=20)


class Email(Document):
    """Elasticsearch Email Object."""

    email_id = Keyword(required=True)
    google_id = Keyword(required=True)
    thread_id = Keyword(required=True)
    sender = Keyword(required=True)
    sender_name = Keyword(required=True)
    sender_address = Keyword(required=True)
    recipient = Keyword(required=True)
    date = Date(required=True)
    subject = Text(analyzer="snowball", required=True)
    plain = Text(analyzer="snowball", required=True)
    html = Text(analyzer="snowball")
    preview = Text(analyzer="snowball")
    labels = Keyword(multi=True)
    line_count = Integer()
    char_count = Integer()

    class Index:
        name = "email"
        settings = {
            "number_of_shards": 1,
        }

    def save(self, **kwargs):
        self.line_count = len(self.plain.split())
        self.chart_count = len(self.plain)
        return super().save(**kwargs)


def from_gmail_dict(email: Dict):
    return Email(
        meta={"id": email["google_id"]},
        email_id=email["email_id"],
        google_id=email["google_id"],
        thread_id=email["thread_id"],
        sender=email["sender"],
        sender_name=email["sender_name"],
        sender_address=email["sender_address"],
        recipient=email["recipient"],
        date=email["date"],
        subject=email["subject"],
        plain=email["plain"],
        html=email["html"],
        label_ids=email["label_ids"],
    )


if __name__ == "__main__":
    # Define a default Elasticsearch client
    connections.create_connection(hosts=["localhost"])

    # create the mappings in elasticsearch
    Email.init()

    # create and save and article
    # email = Email(
    #     meta={"id": 42},
    #     email_id="fake_email_id",
    #     google_id="fake_google_id",
    #     sender="bfortuner@gmail.com",
    #     recipient="jackie@gmail.com",
    #     date=datetime.now(),
    #     subject="Hello world!",
    #     plain="""looong text \n some more \n yo""",
    #     labels=["INBOX"],
    # )
    # email.save()

    # email = email.get(id=42)

    # print(email)

    # Display cluster health
    print(connections.get_connection().cluster.health())
