"""Load and read large .mbox files from Gmail Export.

http://www.relevantmisc.com/scraping/2020/01/29/processing-mbox/


"""
import email
from email.policy import default
import mailbox
import bs4


def getbody(message):  # getting plain text 'email body'
    body = None
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload(decode=True)
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
    elif message.get_content_type() == 'text/plain':
        body = message.get_payload(decode=True)
    return body


class MBoxReader:
    """Stream read very large Mbox file."""
    def __init__(self, filename):
        self.handle = open(filename, 'rb')
        assert self.handle.readline().startswith(b'From ')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.handle.close()

    def __iter__(self):
        return iter(self.__next__())

    def __next__(self):
        lines = []
        while True:
            line = self.handle.readline()
            if line == b'' or line.startswith(b'From '):
                yield email.message_from_bytes(b''.join(lines), policy=default)
                if line == b'':
                    break
                lines = []
                continue
            lines.append(line)


def get_html_text(html):
    try:
        return bs4.BeautifulSoup(html, 'lxml').body.get_text(' ', strip=True)
    except AttributeError: # message contents empty
        return None


class GmailMboxMessage():
    def __init__(self, email_data):
        if not isinstance(email_data, mailbox.mboxMessage):
            raise TypeError('Variable must be type mailbox.mboxMessage')
        self.email_data = email_data

    def parse_email(self):
        return {
            "email_labels": self.email_data['X-Gmail-Labels'],
            "email_date": self.email_data['Date'],
            "email_from": self.email_data['From'],
            "email_to": self.email_data['To'],
            "email_subject": self.email_data['Subject'],
            "email_text": self.read_email_payload(),
        }

    def read_email_payload(self):
        email_payload = self.email_data.get_payload()
        if self.email_data.is_multipart():
            email_messages = list(self._get_email_messages(email_payload))
        else:
            email_messages = [email_payload]
        return [self._read_email_text(msg) for msg in email_messages]

    def _get_email_messages(self, email_payload):
        for msg in email_payload:
            if isinstance(msg, (list, tuple)):
                for submsg in self._get_email_messages(msg):
                    yield submsg
            elif msg.is_multipart():
                for submsg in self._get_email_messages(msg.get_payload()):
                    yield submsg
            else:
                yield msg

    def _read_email_text(self, msg):
        content_type = 'NA' if isinstance(msg, str) else msg.get_content_type()
        encoding = 'NA' if isinstance(msg, str) else msg.get('Content-Transfer-Encoding', 'NA')
        if 'text/plain' in content_type and 'base64' not in encoding:
            msg_text = msg.get_payload()
        elif 'text/html' in content_type and 'base64' not in encoding:
            msg_text = get_html_text(msg.get_payload())
        elif content_type == 'NA':
            msg_text = get_html_text(msg)
        else:
            msg_text = None
        return (content_type, encoding, msg_text)


def get_text(msg):
    while msg.is_multipart():
        msg = msg.get_payload()[0]
    return msg.get_payload()


def remove_r(text):
    return text.replace("\r", "")


def strip_replies(text):
    lines = text.split("\n")
    lines = [l for l in lines if len(l) > 0]
    lines = [line for line in lines if line[0] != ">"]
    return "\n".join(lines)


import re
import sys


def strip_footer(text):
    text, _ = re.subn(
        "On (Sun|Mon|Tue|Wed|Thu|Fri|Sat),.*, 20.. at.*@gmail.com.*wrote.*",
        "",
        text,
        flags=re.DOTALL
    )
    text, _ = re.subn(
        "You received this message because you are subscribed to the Google Groups.*",
        "",
        text,
        flags=re.DOTALL
    )
    return text


def get_member_emails(mbox, sender_list, limit=100):
    msgs = []
    for msg in mbox:
        if (msg["sender"] in sender_list and msg["recipient"] is not None and "friends@example.com" == msg["recipient"]):
            msgs.append(msg)
        if limit is not None and len(msgs) > limit:
            break
    return msgs


def get_core_text(msg):
    msg = get_text(msg)
    msg = remove_r(msg)
    msg = strip_replies(msg)
    msg = strip_footer(msg)
    return msg


def print_msgs(msg_list, f=sys.stdout):
    for msg in msg_list:
        print("--------------------------------", file=f)
        print("Subject:", msg["subject"], file=f)
        print("", file=f)
        print(get_core_text(msg), file=f)
        print("", file=f)



if __name__ == "__main__":
    fpath = "data/google/Mail/Category Travel.mbox"
    fpath = "data/google/Mail/Sent.mbox"
    # fpath = "data/google/Mail/Inbox.mbox"

    # with MBoxReader(fpath) as mbox:
    #     for i, message in enumerate(mbox):
    #         print(message.as_string())
    #         if i > 5:
    #             break
    import pprint

    pp = pprint.PrettyPrinter(indent=2)
    mbox = mailbox.mbox(fpath)
    num_entries = len(mbox)
    print(f"Num Entries {num_entries}")

    # for idx, email_obj in enumerate(mbox):
    #     print('Parsing email {0} of {1}'.format(idx, num_entries))
    #     email_data = GmailMboxMessage(email_obj).parse_email()
    #     print(f"Num Messages: {len(email_data)}")
    #     if email_data["email_text"][0][0] in ("text/plain"):#, "text/html"):
    #         pp.pprint(email_data)

    #     if idx > 10:
    #         break

    for i, msg in enumerate(mbox):
        text = get_core_text(msg)
        print(text)
        if i > 5:
            break
