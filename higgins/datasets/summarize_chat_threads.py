# https://beta.openai.com/playground/p/Ty0rOjsB0YmPYZXDyXUL21JV?model=davinci-instruct-beta

SUMMARIZE_CHAT_THREAD_DATASET_TRAIN = """Summarize the following text messages

CONVERSATION
Brendan: Hey are you free tonight
Jackie: Yeah! What did you have in mine.
Brendan: let's grab dinner. What are you feeling?
Jackie: Let's do mexican
Brendan: Sounds good!

SUMMARY
Jackie and Brendan decide to get mexican food for dinner
<<<END>>

CONVERSATION
Brendan: What time are you coming over tonight?
Jackie: Around 8:30
Brendan: Great. Could you bring my blanket?
Jackie: Okay!

SUMMARY
Jackie is coming over at 8pm. She's going to bring Brendan's blanket
<<<END>>

CONVERSATION
Dave: Hey are you free for a call?
Dave: Would love to chat about the job.
Ling: Yeah! What time?
Dave: how about 10pm.
Ling: I can't do 10. But I'm free tomorrow at 9am?

SUMMARY
Dave asks to chat about the job. Ling proposes tomorrow at 9am
<<<END>>

CONVERSATION
Brendan: got GPT3 to summarize and compose emails
Brendan: and edit the emails
Brendan: crazy 
David: Wow, that's nut.
David: I'm not sure I want to upload my data to Google cloud

SUMMARY
Brendan is impressed with Google's AI. David is not sure about uploading his data to Google Cloud
<<END>>
"""