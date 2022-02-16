SEND_EMAIL_DATASET_TRAIN = [
    {
        "query": "Send an email to mom and let her know I'm coming home for Christmas",
        "actions": [
            {
                "action": "SendEmail",
                "params": {
                    "recipient": "mom",
                    "subject": "Christmas plans",
                    "plain": "I'm coming home for Christmas",
                }
            },
        ]
    },
    {
        "query": "email Brian jennings and ask if I can tour the apartment tomorrow",
        "actions": [
            {
                "action": "SendEmail",
                "params": {
                    "recipient": "Brian jennings",
                    "subject": "Apartment visit",
                    "plain": "Can I tour the apartment tomorrow?",
                }
            },
        ]
    },
    {
        "query": "email support@mattressfirm.com Return my order for a full refund",
        "actions": [
            {
                "action": "SendEmail",
                "params": {
                    "recipient": "support@mattressfirm.com",
                    "subject": "Return Order",
                    "plain": "I would like to schedule a return and receive a full refund",
                }
            },
        ]
    },
    {
        "query": "email Sally can we push our meeting to tomorrow at 9am?",
        "actions": [
            {
                "action": "SendEmail",
                "params": {
                    "recipient": "Sally",
                    "subject": "Raincheck meeting",
                    "plain": "Can we push our meeting to tomorrow at 9am?",
                }
            },
        ]
    },
    {
        "query": "Cancel membership support at netflix.com",
        "actions": [
            {
                "action": "SendEmail",
                "params": {
                    "recipient": "support@netflix.com",
                    "subject": "Cancel membership",
                    "plain": "Can you cancel my membership?",
                }
            },
        ]
    },
]

SEND_EMAIL_DATASET_TEST = [
    {
        "query": "Email Dad and ask if my tennis rackets arrived",
        "actions": [
            {
                "action": "SendEmail",
                "params": {
                    "recipient": "Dad",
                    "subject": "Tennis rackets",
                    "plain": "Have my tennis rackets arrived?",
                }
            },
        ]
    },
    {
        "query": "email mission@bodyrok.edu cancel membership",
        "actions": [
            {
                "action": "SendEmail",
                "params": {
                    "recipient": "mission@bodyrok.edu",
                    "subject": "Cancel membership",
                    "plain": "Can you cancel my membership?",
                }
            },
        ]
    },
]

SEARCH_EMAIL_DATASET_TRAIN = [
    {
        "query": "Get unread emails newer than 1 month old with labels finance and Betterment",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "???",
                    "subject": "???",
                    "unread": "True",
                    "labels": "finance AND Betterment",
                    "exact_phrase": "???",
                    "newer_than": "1 month",
                    # "older_than": "???",
                    # "before": "2/10/2020",
                    # "after": "???",
                    # "has_attachment": "???",
                    # "attachment_spec": "???",
                }
            },
        ]
    },
    {
        "query": "Find emails with the subject Hello Brendan",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "???",
                    "subject": "Hello Brendan",
                    "unread": "???",
                    "labels": "???",
                    "exact_phrase": "???",
                    "newer_than": "???",
                }
            },
        ]
    },
    {
        "query": "Get emails from Dad",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "Dad",
                    "subject": "???",
                    "unread": "???",
                    "labels": "???",
                    "exact_phrase": "???",
                    "newer_than": "???",
                }
            },
        ]
    },
    {
        "query": "Search for emails Erin Fortuner sent in the last 30 days",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "Erin Fortuner",
                    "subject": "???",
                    "unread": "???",
                    "labels": "???",
                    "exact_phrase": "???",
                    "newer_than": "30 day",
                }
            },
        ]
    },
    # {
    #     "query": "Find emails sent to cfortuner@gmail.com",
    #     "actions": [
    #         {
    #             "action": "SearchEmail",
    #             "params": {
    #                 "recipient": "cfortuner@gmail.com",
    #                 "sender": "???",
    #                 "subject": "???",
    #                 "unread": "???",
    #                 "labels": "???",
    #                 "exact_phrase": "???",
    #                 "newer_than": "???",
    #             }
    #         },
    #     ]
    # },
    {
        "query": "Get all unread emails sent in the last 2 days",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "???",
                    "subject": "???",
                    "unread": "True",
                    "labels": "???",
                    "exact_phrase": "???",
                    "newer_than": "2 day",
                }
            },
        ]
    },
    {
        "query": "Find emails which contain the phrase fizzy bottle",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "???",
                    "subject": "???",
                    "unread": "???",
                    "labels": "???",
                    "exact_phrase": "fizzy bottle",
                    "newer_than": "???",
                }
            },
        ]
    },
    {
        "query": "search for emails from nari.kourian@getcruise.ai",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "nari.kourian@getcruise.ai",
                    "subject": "???",
                    "unread": "???",
                    "labels": "???",
                    "exact_phrase": "???",
                    "newer_than": "???",
                }
            },
        ]
    },
]

SEARCH_EMAIL_DATASET_TEST = [
    {
        "query": "Get emails from Jackie First",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "Jackie First",
                    "subject": "???",
                    "unread": "???",
                    "labels": "???",
                    "exact_phrase": "???",
                    "newer_than": "???",
                }
            },
        ]
    },
    {
        "query": "Get emails sent by York Mather in the last month",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "York Mather",
                    "subject": "???",
                    "unread": "???",
                    "labels": "???",
                    "exact_phrase": "???",
                    "newer_than": "1 month"
                }
            },
        ]
    },
    {
        "query": "Find emails titled My first email",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "???",
                    "subject": "My first email",
                    "unread": "???",
                    "labels": "???",
                    "exact_phrase": "???",
                    "newer_than": "???",
                }
            },
        ]
    },
    {
        "query": "Get all emails from Colin sent in the last week",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "Colin",
                    "subject": "???",
                    "unread": "???",
                    "labels": "???",
                    "exact_phrase": "???",
                    "newer_than": "7 day",
                }
            },
        ]
    },
    {
        "query": "Get all unread emails received in the last 5 days",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "???",
                    "subject": "???",
                    "unread": "True",
                    "labels": "???",
                    "exact_phrase": "???",
                    "newer_than": "5 day",
                }
            },
        ]
    },
    {
        "query": "Get all unread emails with the labels tennis OR Federer",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "???",
                    "subject": "???",
                    "unread": "True",
                    "labels": "tennis OR Federer",
                    "exact_phrase": "???",
                    "newer_than": "???",
                }
            },
        ]
    },
    {
        "query": "Get emails with the phrase Yoon Manivanh",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "???",
                    "subject": "???",
                    "unread": "???",
                    "labels": "???",
                    "exact_phrase": "Yoon Manivanh",
                    "newer_than": "???",
                }
            },
        ]
    },
    {
        "query": "Get emails from Yoon Manivanh",
        "actions": [
            {
                "action": "SearchEmail",
                "params": {
                    "recipient": "???",
                    "sender": "Yoon Manivanh",
                    "subject": "???",
                    "unread": "???",
                    "labels": "???",
                    "exact_phrase": "???",
                    "newer_than": "???",
                }
            },
        ]
    },
]

# Compose prompt: https://beta.openai.com/playground/p/MOuS7ocSyR4KEhjtlGb6rbMq?model=davinci-instruct-beta
# Summarize prompt: https://beta.openai.com/playground/p/jMjBhqKd9DOvbB6u71ydNRIn?model=davinci
COMPOSE_EMAIL_DATASET_TRAIN = [
    {
        "query": "Send email to mom and let her know I'm coming home for Christmas",
        "actions": [
            {
                "action": "ComposeEmail",
                "params": {
                    "recipient": "mom",
                    "subject": "Christmas plans",
                    "plain": "I'm coming home for Christmas.",
                }
            },
        ],
        "summary": "Coming home for Christmas",
    },
    {
        "query": "Send an email to mission@bodyrok.com. Ask to pause membership starting this Thursday and resume in October. Explain my reason is I'm leaving for an RV trip for 1-2 months.",
        "actions": [
            {
                "action": "ComposeEmail",
                "params": {
                    "recipient": "mission@bodyrok.com",
                    "subject": "Pause membership",
                    "plain": "Is it possible to pause my membership starting Thursday? And resume the membership in October. I'm leaving for an RV trip for 1-2 months and won't be back until October. Thanks!",
                }
            },
        ],
        "summary": "Asking to pause their Bodyrok membership",
    },
    {
        "query": "Compose email. Ask if he has the tennis tickets and whether he'd like me to pay. If so, how much. Which payment method. I'm looking forward to getting together!",
        "actions": [
            {
                "action": "ComposeEmail",
                "params": {
                    "recipient": "???",
                    "subject": "Tennis tickets",
                    "plain": "Did you get the tennis tickets? Let me know if you want me to pay! If you do, let me know how much and how I can pay you. Venmo?",
                }
            },
        ],
        "summary": "They asked about the tennis tickets and how to pay you.",
    },
    {
        "query": "Email my manager and let her know I've decided to leave Cruise. Flexible on when I leave. It's up to her. I'd like to stick around at least until October 15 when my vest day is.",
        "actions": [
            {
                "action": "ComposeEmail",
                "params": {
                    "recipient": "my manager",
                    "subject": "Leaving Cruise",
                    "plain": "I've decided to leave Cruise. I'm flexible on when I leave. It's up to you. I would like to stick around until October 15 when my vest day is.",
                }
            },
        ],
        "summary": "They are planning to leave Cruise on October 15."
    },
    {
        "query": "Email Amazon Customer Service. Ask them when my order will arrive. Order number akjgs-1726-j298.",
        "actions": [
            {
                "action": "ComposeEmail",
                "params": {
                    "recipient": "Amazon Customer Service",
                    "subject": "Delivery estimate",
                    "plain": "Do you know when my order will arrive. My order number is akjgs-1726-j298.",
                }
            },
        ],
        "summary": "Wants to know when their order will arrive."
    },
    {
        "query": "Email David Ling. Hope you're well. Tell him I've accepted the job offer at Cruise. Starting salary: 100k. Is that good?",
        "actions": [
            {
                "action": "ComposeEmail",
                "params": {
                    "recipient": "David Ling",
                    "subject": "Accepted Cruise Job Offer",
                    "plain": "Hope you're well. I accepted the Cruise job offer. Is 100k a good base salary?",
                }
            },
        ],
        "summary": "They accepted the Cruise job offer and have a question about salary."
    },
    {
        "query": "Email Dad and ask if he's coming over for dinner",
        "actions": [
            {
                "action": "ComposeEmail",
                "params": {
                    "recipient": "Dad",
                    "subject": "Dinner?",
                    "plain": "Are you coming over for dinner?",
                }
            },
        ],
        "summary": "Asked about dinner plans"
    },
    {
        "query": "Inform Ling her order has shipped and will arrive in 2 days. Order status link: <a href='www.amazon.com/order/12786543765'>here</a>",
        "actions": [
            {
                "action": "ComposeEmail",
                "params": {
                    "recipient": "Ling",
                    "subject": "Order status",
                    "plain": "This message is to inform you that your product has shipped! It will arrive in 2 days. Check your order status <a href='www.amazon.com/order/12786543765'>here</a>.",
                }
            },
        ],
        "summary": "Your Amazon order will arrive in 2 days."
    },
    # {
    #     "query": "Cancel membership support at netflix.com",
    #     "actions": [
    #         {
    #             "action": "SendEmail",
    #             "params": {
    #                 "recipient": "support@netflix.com",
    #                 "subject": "Cancel membership",
    #                 "plain": "Can you cancel my membership?",
    #             }
    #         },
    #     ],
    #     "summary": "Asks to cancel netflix membership"
    # },
    {
        "query": "email Sally can we push our meeting to tomorrow at 9am?",
        "actions": [
            {
                "action": "ComposeEmail",
                "params": {
                    "recipient": "Sally",
                    "subject": "Raincheck meeting",
                    "plain": "Can we push our meeting to tomorrow at 9am?",
                }
            },
        ],
        "summary": "Wants to push the meeting to 9am tomorrow"
    },
]

COMPOSE_EMAIL_DATASET_TEST = [
    {
        "query": "Email Lumen Support with my fedex tracking number. Number is 175452902. Let them know I filled out the form. Ask when I'll get the refund.",
        "actions": [
            {
                "action": "ComposeEmail",
                "params": {
                    "recipient": "Lumen Support",
                    "subject": "Refund",
                    "plain": "I filled out the form. My Fedex tracking number is 175452902. When will I get the refund?",
                }
            },
        ],
        "summary": "Asking about the status of their refund."
    },
    {
        "query": "Compose an email to Colin and let him know I'm coming to Alaska. I've thought it over and decided it seems fun. Tell him I'll start looking for flights. And ask when he's flying out.",
        "actions": [
            {
                "action": "ComposeEmail",
                "params": {
                    "recipient": "Colin",
                    "subject": "Alaska trip",
                    "plain": "I wanted to let you know I've decided to come to Alaska! It seems fun. I'll start looking for flights now. Could you let me know when your flight is?",
                }
            },
        ],
        "summary": "They're coming to Alaska and asked about your flight schedule."
    },
]

# https://beta.openai.com/playground/p/bgFErKOAwhe5j9o7w3jI3Ynz?model=davinci-instruct-beta
EDIT_EMAIL_DATASET_TRAIN = [
    {
        "actions": [
            {
                "action": "EditEmail",
                "params": {
                    "recipient": "mission@bodyrok.com",
                    "subject": "Pause membership",
                    "user_text": "Send an email to mission@bodyrok.com. Ask to pause membership starting this Thursday and resume in October. Explain my reason is I'm leaving for an RV trip for 1-2 months.",
                    "first_draft": "Hello Bodyrok Mission,\nIs it possible to pause my membership starting Thursday? And resume the membership in October. I'm leaving for an RV trip for 1-2 months and won't be back until October.\nBrendan",
                    "feedback": "Replace Bodyrok Mission with team. Change Thursday to Friday the 14th. Remove the line about the RV trip. Change the signature to Thanks, Brendan",
                }
            },
        ],
        "revised_email": "Hello team,\nIs it possible to pause my membership starting Friday the 14th? And resume the membership in October.\nThanks,\nBrendan",
    },
    {
        "actions": [
            {
                "action": "EditEmail",
                "params": {
                    "recipient": "Colin Fortuner",
                    "subject": "Alaska trip",
                    "user_text": "Send an email to Colin and let him know I'm coming to Alaska. I've thought it over and decided it seems fun. Tell him I'll start looking for flights. And ask when he's flying out.",
                    "first_draft": "Hi Colin Fortuner,\nI wanted to let you know I've decided to come to Alaska! It seems fun. I'll start looking for flights know. Could you let me know when your flight is?",
                    "feedback": "Replace Colin Fortuner with Cols. Add hope you're well at the beginning. Add From, Brendan.",
                }
            },
        ],
        "revised_email": "Hi Cols,\nHope you're well! I wanted to let you know I've decided to come to Alaska! It seems fun. I'll start looking for flights know. Could you let me know when your flight is?\nFrom,\nBrendan",
    },
    {
        "actions": [
            {
                "action": "EditEmail",
                "params": {
                    "recipient": "Amazon Customer Service",
                    "subject": "Delivery estimate",
                    "user_text": "Email Amazon Customer Service. Ask them when my order will arrive. Order number akjgs-1726-j298.",
                    "first_draft": "Do you know when my order will arrive?",
                    "feedback": "Ask them for a tracking number. Add my order id.",
                }
            },
        ],
        "revised_email": "Do you know when my order will arrive? My order number is akjgs-1726-j298. And can you provide me a tracking number?",
    },
    {
        "actions": [
            {
                "action": "EditEmail",
                "params": {
                    "recipient": "Ling",
                    "subject": "Leaving Cruise",
                    "user_text": "Email my manager Ling and let her know I've decided to leave Cruise. Flexible on when I leave. It's up to her. I'd like to stick around at least until October 15 when my vest day is.",
                    "first_draft": "Hi Ling, I've decided to leave Cruise. I'm flexible on when I leave. It's up to you. I would like to stick around until October 15 when my vest day is.",
                    "feedback": "Remove Hi Ling. Change October 15 to November 4",
                }
            },
        ],
        "revised_email": "I've decided to leave Cruise. I'm flexible on when I leave. It's up to you. I would like to stick around until November 4 when my vest day is.",
    },
]

EDIT_EMAIL_DATASET_TEST = [
    {
        "actions": [
            {
                "action": "EditEmail",
                "params": {
                    "recipient": "Lumen Support",
                    "subject": "Refund",
                    "user_text": "Reply to Lumen Support and paste my fedex tracking number 175452902. Let them know I filled out the form. Ask when I'll get the refund.",
                    "first_draft": "Hi Lumen Support,\nI filled out the form. When will I get the refund?\nStew",
                    "feedback": "Add my fedex tracking number. Change the intro to Hi team. Add Are you open today? to the beginning.",
                }
            },
        ],
        "revised_email": "Hi team,\nAre you open today? I filled out the form. When will I get the refund? My fedex tracking number is 175452902.\nStew",
    },
    {
        "actions": [
            {
                "action": "EditEmail",
                "params": {
                    "recipient": "Bill Fortuner",
                    "subject": "Tennis tickets payment",
                    "user_text": "Email Bill Fortuner. Ask if he has the tennis tickets and whether he'd like me to pay. If so, how much. Which payment method. I'm looking forward to getting together!",
                    "first_draft": "Hey Bill,\nDid you get the tennis tickets? Let me know if you want me to pay! If you do, let me know how much and how I can pay you. Venmo?\nJackie First",
                    "feedback": "Replace Hey Bill with Dad. Add Paypal as a payment option.",
                }
            },
        ],
        "revised_email": "Dad,\nDid you get the tennis tickets? Let me know if you want me to pay! If you do, let me know how much and how I can pay you. Venmo or Paypal?\nJackie First",

    },
]

COMPOSE_EMAIL_DATASET = []
COMPOSE_EMAIL_DATASET.append(COMPOSE_EMAIL_DATASET_TRAIN)
COMPOSE_EMAIL_DATASET.append(COMPOSE_EMAIL_DATASET_TEST)

EMAIL_DATASETS_TRAIN = []
EMAIL_DATASETS_TRAIN += SEND_EMAIL_DATASET_TRAIN
EMAIL_DATASETS_TRAIN += SEARCH_EMAIL_DATASET_TRAIN
EMAIL_DATASETS_TRAIN += COMPOSE_EMAIL_DATASET_TRAIN

EMAIL_DATASETS_TEST = []
EMAIL_DATASETS_TEST += SEND_EMAIL_DATASET_TEST
EMAIL_DATASETS_TEST += SEARCH_EMAIL_DATASET_TEST
EMAIL_DATASETS_TRAIN += COMPOSE_EMAIL_DATASET_TEST
