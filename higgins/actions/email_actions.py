from copy import deepcopy
from pprint import PrettyPrinter
import time
from typing import Callable, Dict, List

from higgins.actions import Action, ActionParam, ActionParamSpec, ActionResult
from higgins.actions import contact_actions
from higgins.automation.google import gmail
from higgins.automation.email import email_utils
from higgins.database import tiny
from higgins.nlp.openai import data_question_completions
from higgins.nlp.openai import email_completions
from higgins.nlp import nlp_utils

pp = PrettyPrinter(indent=2)


class EmailAction(Action):

    def __init__(self, params: Dict = None, db=None):
        super().__init__(params)
        self.db = db

    def add_automations(self, automations: Dict) -> Dict:
        if "db" not in automations:
            automations["db"] = tiny.load_database()
        self.db = automations["db"]
        return automations


class SendEmail(EmailAction):

    def __init__(self, params: Dict = None, db=None, contact_info=None):
        super().__init__(params, db)
        self.contact_info = contact_info

    @classmethod
    def param_specs(cls):
        return {
            "recipient": ActionParamSpec(name="recipient", question="Who would you like to email?", required=True),
            "subject": ActionParamSpec(name="subject", question="What is the subject?", required=True),
            "plain": ActionParamSpec(name="plain", question="What should the email body contain?", required=True),
        }

    def clarify(self, prompt_fn: Callable) -> List[str]:
        name = self.params["recipient"].value.strip()
        if not email_utils.is_valid_email(name):
            contact_info = contact_actions.clarify_contact_info(
                name=name, db=self.db, prompt_fn=prompt_fn
            )
            self.params["recipient"].value = contact_info.email
        super().clarify(prompt_fn)

    def run(self):
        body = self.params["plain"].value
        return ActionResult(
            action_text=f"Emailing message '{body}' to {self.params['recipient'].value}"
        )


class ComposeEmail(EmailAction):

    def __init__(self, params: Dict = None, db=None, contact_info=None):
        super().__init__(params, db)
        self.contact_info = contact_info

    @classmethod
    def param_specs(cls):
        return {
            "recipient": ActionParamSpec(name="recipient", question="Who would you like to email?", required=True),
            "subject": ActionParamSpec(name="subject", question="What is the subject?", required=True),
            "plain": ActionParamSpec(name="plain", question="What should the email body contain?", required=True),
            "user_text": ActionParamSpec(name="user_text", question=""),
        }

    def clarify(self, prompt_fn: Callable) -> List[str]:
        name = self.params["recipient"].value.strip()
        if not email_utils.is_valid_email(name):
            contact_info = contact_actions.clarify_contact_info(
                name=name, db=self.db, prompt_fn=prompt_fn
            )
            self.params["recipient"].value = contact_info.email

    def run(self):
        email = {k: p.value for k, p in self.params.items()}
        return ActionResult(
            reply_text=email_utils.get_email_preview(email),
            data=email,
            reply_handler_classname="ComposeEmailReplyHandler",
        )


class EditEmail(EmailAction):

    def __init__(self, params: Dict = None, db=None, contact_info=None):
        super().__init__(params, db)
        self.contact_info = contact_info

    @classmethod
    def param_specs(cls):
        return {
            "recipient": ActionParamSpec(name="recipient", question="Who would you like to email?", required=True),
            "subject": ActionParamSpec(name="subject", question="What is the subject?", required=True),
            "user_text": ActionParamSpec(name="plain", question="What was the user's original request?", required=True),
            "first_draft": ActionParamSpec(name="data", question="What was the first draft?", required=True),
            "feedback": ActionParamSpec(name="data", question="What would you like to change?", required=True),
        }

    def clarify(self, prompt_fn: Callable) -> List[str]:
        super().clarify(prompt_fn)

    def run(self):
        answer = email_completions.edit_email_completion(
            user_text=self.params["user_text"].value,
            first_draft=self.params["first_draft"].value,
            feedback=self.params["feedback"].value,
        )
        data = {
            "recipient": self.params["recipient"].value,
            "subject": self.params["subject"].value,
            "plain": answer,
            "user_text": self.params["user_text"].value,
        }
        return ActionResult(
            reply_text=email_utils.get_email_preview(data),
            data=data,
            reply_handler_classname="ComposeEmailReplyHandler",
        )


class SearchEmail(EmailAction):

    @classmethod
    def param_specs(cls):
        return {
            "recipient": ActionParamSpec(name="recipient", question=""),
            "sender": ActionParamSpec(name="sender", question=""),
            "subject": ActionParamSpec(name="subject", question=""),
            "unread": ActionParamSpec(name="unread", question=""),
            "labels": ActionParamSpec(name="labels", question=""),
            "exact_phrase": ActionParamSpec(name="exact_phrase", question=""),
            "newer_than": ActionParamSpec(name="newer_than", question=""),
        }

    def clarify(self, prompt_fn: Callable) -> List[str]:
        super().clarify(prompt_fn)
        recipient = self.params["recipient"].value
        if recipient and not email_utils.is_valid_email(recipient):
            recipient_info = contact_actions.clarify_contact_info(
                name=recipient, db=self.db, prompt_fn=prompt_fn, loop_until_found=False,
            )
            if recipient_info is not None:
                self.params["recipient"].value = recipient_info.email

        sender = self.params["sender"].value
        if sender and not email_utils.is_valid_email(sender):
            sender_info = contact_actions.clarify_contact_info(
                name=sender, db=self.db, prompt_fn=prompt_fn, loop_until_found=False,
            )
            if sender_info is not None:
                self.params["sender"].value = sender_info.email

    def run(self):
        query = action_params_to_query(self.params)
        emails = gmail.search_emails(query_dicts=[query])
        reply_handler = "SearchEmailReplyHandler" if len(emails) > 0 else None
        return ActionResult(
            action_text=f"Found {len(emails)} emails using query {query}.",
            reply_text=email_utils.get_email_list_preview(emails) if emails else None,
            data=emails,
            reply_handler_classname=reply_handler,
        )


class AnswerEmailQuestion(EmailAction):

    def add_automations(self, automations: Dict) -> Dict:
        super().add_automations(automations)
        if "tokenizer" not in automations:
            automations["tokenizer"] = nlp_utils.get_tokenizer()
        self.tokenizer = automations["tokenizer"]
        return automations

    @classmethod
    def param_specs(cls):
        return {
            "data": ActionParamSpec(name="data", question="What data would you like to parse?", required=True),
            "question": ActionParamSpec(name="question", question="What is your question?", required=True),
        }

    def clarify(self, prompt_fn: Callable) -> List[str]:
        super().clarify(prompt_fn)
        data = self.params["data"].value
        if isinstance(data, list):
            if len(data) == 0:
                self.params["data"].value = None
            elif len(data) == 1:
                self.params["data"].value = data[0]
            else:
                index = None
                while index is None:
                    index = int(prompt_fn(f"{len(data)} emails found. Which one to query? Index number (0-{len(data)-1}): "))
                    if index < 0 or index >= len(data):
                        index = None
                self.params["data"].value = data[index]
        else:
            assert data is None or isinstance(data, dict), "Must be dict or list or None"

    def _trim_tokens(self, text: str):
        # OpenAI doesn't support completions with context > 2049 tokens, which includes the completion tokens (100-300)
        MAX_BODY_TOKENS = 1024  # https://beta.openai.com/tokenizer
        text = text.replace("\n", " ")
        # print("num tokens", nlp_utils.get_num_tokens(data["plain"], self.tokenizer))
        text = nlp_utils.trim_tokens(
            text=text, max_tokens=MAX_BODY_TOKENS, tokenizer=self.tokenizer
        )
        return text

    def _ask_data_question(self, question: str, data: Dict) -> str:
        data = deepcopy(data)
        data["plain"] = self._trim_tokens(data["plain"])
        answer = data_question_completions.data_question_completion(
            question=question, data=data
        )
        return answer

    def _summarize_email(self, data: Dict) -> str:
        text = self._trim_tokens(data["plain"])
        return email_completions.summarize_email_completion(email_body=text)

    def run(self):
        data = self.params["data"].value
        question = nlp_utils.normalize_text(self.params["question"].value)
        if not data:  # None or empty list:
            return ActionResult(status="failed", reply_text="No emails matched your search.")

        stats = email_utils.get_body_stats(data["plain"])
        # print(f"Email stats: {stats}")

        if "preview" in question or "snippet" in question:
            answer = email_utils.get_email_preview(data, max_lines=10)
        elif question in ["show email", "display email", "show body", "show text"]:
            answer = email_utils.get_email_preview(data)
        elif "summarize" in question:
            answer = self._summarize_email(data)
        else:
            answer = self._ask_data_question(question, data)

        return ActionResult(
            reply_text=answer,
            data=self.params["data"].value,
            reply_handler_classname="SearchEmailReplyHandler"
        )


def action_params_to_query(params: Dict[str, ActionParam]) -> List[Dict]:
    query = {}
    if params["recipient"].value is not None:
        query["recipient"] = params["recipient"].value
    if params["sender"].value is not None:
        query["sender"] = params["sender"].value
    if params["newer_than"].value is not None:
        field_name, field_value = email_utils.format_newer_than_param(params["newer_than"].value)
        query[field_name] = field_value
    if params["unread"].value is not None:
        query["unread"] = True
    if params["subject"].value is not None:
        query["subject"] = params["subject"].value
    if params["exact_phrase"].value is not None:
        query["exact_phrase"] = params["exact_phrase"].value
    if params["labels"].value is not None:
        labels = params["labels"].value
        if " AND " in labels:
            labels = labels.split(" AND ")
        elif " OR " in labels:
            labels = [[label] for label in labels.split(" OR ")]
        query["labels"] = labels

    return query
