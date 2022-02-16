SEND_MESSAGE_DATASET_TRAIN = [
    {
        "query": "Text mom I love her",
        "actions": [
            {
                "action": "SendMessage",
                "params": {
                    "recipient": "mom",
                    "body": "I love her",
                    "application": "???"
                }
            },
        ]
    },
    {
        "query": "text message steve and ask if he's coming to the meeting",
        "actions": [
            {
                "action": "SendMessage",
                "params": {
                    "recipient": "steve",
                    "body": "Are you coming to the meeting?",
                    "application": "???"
                }
            },
        ]
    },
    {
        "query": "msg Jackie and let her know I'll be home by 10 tonight",
        "actions": [
            {
                "action": "SendMessage",
                "params": {
                    "recipient": "Jackie",
                    "body": "I'll be home by 10pm",
                    "application": "???"
                }
            },
        ]
    },
    {
        "query": "text Colin on Facebook Messenger and ask him if he's free for tennis tomorrow",
        "actions": [
            {
                "action": "SendMessage",
                "params": {
                    "recipient": "Colin",
                    "body": "Are you free for tennis tomorrow?",
                    "application": "Facebook Messenger"
                }
            },
        ]
    },
    {
        "query": "Want to hang out tonight?",
        "actions": [
            {
                "action": "SendMessage",
                "params": {
                    "recipient": "???",
                    "body": "Do you want to hang out tonight?",
                    "application": "???"
                }
            },
        ]
    },
    {
        "query": "Reply to Sam Fortuner on WhatsApp",
        "actions": [
            {
                "action": "SendMessage",
                "params": {
                    "recipient": "Sam Fortuner",
                    "body": "???",
                    "application": "WhatsApp"
                }
            },
        ]
    },
    {
        "query": "slack Sean Bean and tell him I'm running late to the meeting",
        "actions": [
            {
                "action": "SendMessage",
                "params": {
                    "recipient": "Sean Bean",
                    "body": "I'm running late to the meeting",
                    "application": "Slack"
                }
            },
        ]
    },
    {
        "query": "Let Hari know I just pushed my latest changes to the github repo",
        "actions": [
            {
                "action": "SendMessage",
                "params": {
                    "recipient": "Hari",
                    "body": "I pushed my latest changes to the repo",
                    "application": "???"
                }
            },
        ]
    },
    {
        "query": "tell Dad I'll see him next month",
        "actions": [
            {
                "action": "SendMessage",
                "params": {
                    "recipient": "Dad",
                    "body": "I'll see you next month",
                    "application": "???"
                }
            },
        ]
    },
    {
        "query": "Reply Sounds fun!",
        "actions": [
            {
                "action": "SendMessage",
                "params": {
                    "recipient": "???",
                    "body": "Sounds fun!",
                    "application": "???"
                }
            },
        ]
    },
]

SEND_MESSAGE_DATASET_TEST = [
    {
        "query": "message Liam Briggs and see if he wants to get together",
        "actions": [{'action': 'SendMessage', 'params': {'recipient': 'Liam Briggs', 'body': 'Do you want to get together?', 'application': '???'}}]
    },
    {
        "query": "whatsapp Kabir how are you doing?",
        "actions": [{'action': 'SendMessage', 'params': {'recipient': 'Kabir', 'body': 'How are you doing?', 'application': 'WhatsApp'}}]
    },
    {
        "query": "Can you ping Joe Boring and say thanks",
        "actions": [{'action': 'SendMessage', 'params': {'recipient': 'Joe Boring', 'body': 'Thanks', 'application': '???'}}]
    },
    {
        "query": "msg Stew on Slack are you coming to Burning man?",
        "actions": [{'action': 'SendMessage', 'params': {'recipient': 'Stew', 'body': 'Are you coming to Burning Man?', 'application': 'Slack'}}]
    },
    {
        "query": "text Colin on iMessage and see if he's still going to the store",
        "actions": [{'action': 'SendMessage', 'params': {'recipient': 'Colin', 'body': 'Are you still going to the store?', 'application': 'iMessage'}}]
    },
    {
        "query": "This is something isn't it",
        "actions": [{'action': 'SendMessage', 'params': {'recipient': '???', 'body': "This is something isn't it", 'application': '???'}}]
    },
]


MESSAGING_DATASET_TRAIN = []
MESSAGING_DATASET_TRAIN.append(SEND_MESSAGE_DATASET_TRAIN)
