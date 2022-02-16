# nlp

This package includes all the code for speech recognition, speech synthesis, and natural language understanding. It will have both offline and online versions available, depending on the accuracy required or network connectivity. In many cases, the offline models will work well. But if they fail, we can have a fallback mechanism to query a Cloud API for better results.

Example layout

```txt
nlp/
    speech2text/
        offline_listener.py
        google_listener.py
        siri_listener.py
    text2speech/
        offline_voice.py
        Google_voice.py
    summarization/
        offline_summary.py
        azure_summary.py
    utils/
        text_cleaning.py
```
