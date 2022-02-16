"""Datasets for asking questions about data structions."""


DATA_QUESTION_DATASET_TRAIN = [
    {
        "data": {"timestamp": "198738653752", "product_id": "a138764-29877", "title": "Soap, 4 count (pack of 5)", "description": "This is a great body wash soap for men. Good for showering and washing face", "brand_name": "Dove"},
        "questions": [
            ("What is the product id?", "a138764-29877"),
            ("What is the brand?", "Dove"),
            ("This is cool", "???"),
            ("Is it body wash soap?", "Yes"),
            ("What time was it listed?", "198738653752"),
            ("Summarize the description", "This is a great body wash soap for men. Good for showering and washing face"),
            ("What is the pack size?", "5")
        ]
    },
    {
        "data": {"name": "liam.fortuner@gmail.com", "time": "January 15, 2020", "subject": "Used Car", "plain": "I'm interested in buying the car you posted on craigslist. You can reach me at 860-459-8424"},
        "questions": [
            ("When was the message sent?", "January 15, 2020"),
            ("Who's it from?", "liam.fortuner@gmail.com"),
            ("What's his phone number?", "860-459-8424"),
            ("What is Frank name", "???"),
            ("Is he interested in buying the car?", "Yes"),
            ("What's the email about?", "Used Car"),
            ("Display the email text", "I'm interested in buying the car you posted on craigslist. You can reach me at 860-459-8424"),
        ],
    },
    {
        "data": {"name": "Colin", "time": "March 1, 2020", "subject": "What's up bro", "plain": "Just wanted to see how you're doing"},
        "questions": [
            ("When did he send the message?", "March 1, 2020"),
            ("Who sent it?", "Colin"),
            ("What is the subject?", "What's up bro"),
            ("What did he say?", "Just wanted to see how you're doing"),
            ("0", "???"),
        ]
    },
]

DATA_QUESTION_DATASET_TEST = [
    {
        "data": {"name": "Bill Fortuner", "time": "February 20, 2021", "subject": "Tennis tickets for Switzerland", "plain": "Hey Brendan, Would you like to come to the tennis match in April? If so, can you send me $200 for the tickets? Love, Dad"},
        "questions": [
            ("Who sent the message?", "Bill Fortuner"),
            ("When did it arrive?", "February 20, 2021"),
            ("What is the subject of the email?", "Tennis tickets for Switzerland"),
            ("Who should I marry?", "???"),
            ("Display the email text", "Hey Brendan, Would you like to come to the tennis match in April? If so, can you send me $200 for the tickets? Love, Dad"),
        ]
    },
    # {
    #     "data": {"name": "Bill Fortuner", "time": "February 20, 2021", "subject": "Tennis tickets for Switzerland", "plain": "Hey Brendan, Would you like to come to the tennis match in April? If so, can you send me $200 for the tickets? Love, Dad"},
    #     "questions": [
    #         ("Who sent the message?", "Bill Fortuner"),
    #         ("When did it arrive?", "February 20, 2021"),
    #         ("What is the subject of the email?", "Tennis tickets for Switzerland"),
    #         ("Display the email text", "Hey Brendan, Would you like to come to the tennis match in April? If so, can you send me $200 for the tickets? Love, Dad"),
    #     ]
    # }
]

DATA_QUESTION_DATASET = []
DATA_QUESTION_DATASET += DATA_QUESTION_DATASET_TRAIN
DATA_QUESTION_DATASET += DATA_QUESTION_DATASET_TEST
