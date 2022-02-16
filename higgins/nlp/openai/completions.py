# Fine-tune Curie on https://github.com/daveshap/NLCA_Question_Generator
# model_id = ft-YMaOF6HNpubqL2FsWM0yAlGt

import os

import openai

from higgins.nlp.openai import OPENAI_CACHE_DIR

from higgins import const


COMPLETION_CACHE_FILE = os.path.join(OPENAI_CACHE_DIR, "completions.json")

openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_IMPORTANT = """Write a list of the most important and salient questions an observer would ask about the following passage:

PASSAGE:
{text}
END PASSAGE

IMPORTANT OBSERVER QUESTIONS:
-"""
PROMPT_PROCEDURAL = """Write a list of procedural and task-oriented questions about the following passage:

PASSAGE:
{text}
END PASSAGE

PROCEDURAL AND TASK-ORIENTED QUESTIONS:
-"""
PROMPT_TEXT_MESSAGE = """Write a list of clarifying questions about the following message:

MESSAGE:
{text}
END MESSAGE

LIST OF CLARIFYING QUESTIONS:
-"""


# Trained to write clarifying questions given some text, paragraph, dialog..
ft_model_id = "curie:ft-user-7rs1dte2m2824vd5bddi84s8-2021-08-30-21-28-18"
# openai api completions.create -m curie:ft-user-7rs1dte2m2824vd5bddi84s8-2021-08-30-21-28-18 -p <YOUR_PROMPT>


def generate_questions_finetune(
    prompt, model, temp=0.5, top_p=0.95, tokens=60, freq_pen=0.2, pres_pen=0.2, stop=['<<END>>']
):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    return response['choices'][0]['text'].strip().splitlines()


def generate_questions_base(prompt, engine, temp=0.9, top_p=0.95, tokens=200, freq_pen=0.5, pres_pen=0.5, stop=['\n\n']):
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['text'].strip().split("\n-")
    return text


def generate_questions(text: str, mode="finetune"):
    if mode == "finetune":
        prompt = f"{text}\nQUESTIONS:"
        print(f"prompt: {prompt}")
        questions = generate_questions_finetune(prompt, ft_model_id)
    elif mode == "important":
        prompt = PROMPT_IMPORTANT.format(text=text)
        questions = generate_questions_base(prompt, engine="davinci-instruct-beta")
    elif mode == "procedural":
        prompt = PROMPT_TEXT_MESSAGE.format(text=text)
        questions = generate_questions_base(prompt, engine="davinci-instruct-beta")
    return questions


def first_person_to_third_person(text, model="davinci"):
    PROMPT = f"""First-person to third-person

    Input: I decided to make a movie about Ada Lovelace.
    Output: He decided to make a movie about Ada Lovelace.

    Input: My biggest fear was that I wasn't able to write the story adequately.
    Output: His biggest fear was that he wouldn't be able to write the story adequately.

    Input: {text}
    Output:"""
    response = openai.Completion.create(
        engine=model,
        prompt=PROMPT,
        temperature=0.3,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    print(response)
    text = response['choices'][0]['text'].strip()
    return text


def third_person_to_second_person(text, model="davinci"):
    PROMPT = f"""Third-person to second-person

    Input: Brendan decided to make a movie about Ada Lovelace.
    Output: You decided to make a movie about Ada Lovelace.

    Input: What does Janelle want to do with her life?
    Output: What do you want to do with your life?

    Input: His biggest fear was that he wouldn't be able to write the story adequately.
    Output: Your biggest fear was that you wouldn't be able to write the story adequately.

    Input: {text}
    Output:"""
    response = openai.Completion.create(
        engine=model,
        prompt=PROMPT,
        temperature=0.3,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    text = response['choices'][0]['text'].strip()
    return text


def open_ended_chat(chat_history, username=const.USERNAME, agent_name=const.AGENT_NAME, engine="davinci"):
    prompt = f"""The following is a chat between {username} and his personal assistant {agent_name}. {agent_name} only asks {username} clarifying questions to better understand {username}'s intent.
    \n{chat_history}\n{agent_name}:"""
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["\n", " Higgins:"]
    )
    return response.choices[0]["text"].strip()


def summarize_model(prompt: str, engine="davinci"):
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=0.2,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.2,
        presence_penalty=0.0,
    )
    answer = response["choices"][0]["text"]
    return answer
