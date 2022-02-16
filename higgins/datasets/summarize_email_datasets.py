"""Summarize the following emails.

"""

SUMMARIZE_EMAIL_DATASET_TRAIN = [
    {
        "actions": [
            {
                "action": "SummarizeEmail",
                "params": {
                    "plain": "",
                }
            },
        ],
        "summary": "Brendan is looking to pause his Bodyrok membership",
    },
]



EMAIL
Hello,
Is it possible to pause my membership starting Thursday? And resume the membership in October. I'm leaving for an RV trip for 1-2 months and won't be back until October. Thanks!
Brendan

SUMMARY
Brendan is looking to pause his membership
<<END>>

EMAIL
I wanted to let you know I've decided to come to Alaska! It seems fun. I'll start looking for flights know. Could you let me know when your flight is?

SUMMARY
They're coming to Alaska and asked about your flight schedule.
<<END>>

EMAIL
Hey Bill,
Did you get the tennis tickets? Let me know if you want me to pay! If you do, let me know how much and how I can pay you. Venmo?
Mom

SUMMARY
Mom asked about the tennis tickets and how to pay you.
<<END>>

EMAIL
Hi Xin,
I've decided to leave Cruise. I'm flexible on when I leave. It's up to you. I would like to stick around until October 15 when my vest day is.
From,
John Sanborn

SUMMARY
John Sanborn is going to leave Cruise. He wants to stay at Cruise until October.
<<END>>

EMAIL
Hi Lumen Support,
I filled out the form. Here is my Fedex tracking number: 175452902. When will I get the refund?
Joanna

SUMMARY
Joanna is asking about the status of her refund.
<<END>>

EMAIL
Hi Ling,
This message is to inform you that your product has shipped! It will arrive in 2 days. Check your order status <a href="www.amazon.com/order/12786543765">here</a>.
Amazon.com

SUMMARY
Ling's product has shipped.
"""