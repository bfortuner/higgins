# OpenAI API integrations

## Setup

Join the [waitlist](https://openai.com/blog/openai-api/). And you should get access within 48 hours.

Add your API key to `.env.secret` (will be picked up by dotenv, and file not added to git)

```bash
OPENAI_API_KEY="YOUR_KEY"
```

## Examples

Sentiment classification

```bash
This is a tweet sentiment classifier
Tweet: "I loved the new Batman movie!"
Sentiment: Positive
###
Tweet: "I hate it when my phone battery dies." 
Sentiment: Negative
###
Tweet: "My day has been 👍"
Sentiment: Positive
###
Tweet: "This is the link to the article"
Sentiment: Neutral
###
Tweet: "This new music video blew my mind"
Sentiment: 
```

## Links

* https://beta.openai.com/dashboard
* https://beta.openai.com/examples
* https://github.com/OthersideAI/chronology
