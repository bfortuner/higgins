from typing import Callable, Dict, List

from higgins.actions import Action, ActionParamSpec, ActionResult
from higgins.actions import contact_actions
from higgins.database import tiny


class MessagingAction(Action):

    def __init__(self, params: Dict = None, db=None):
        super().__init__(params)
        self.db = db

    def add_automations(self, automations: Dict) -> Dict:
        if "db" not in automations:
            automations["db"] = tiny.load_database()
        self.db = automations["db"]
        return automations


class SendMessage(MessagingAction):

    def __init__(self, params: Dict = None, db=None, contact_info=None):
        super().__init__(params, db)
        self.contact_info = contact_info

    @classmethod
    def param_specs(cls):
        return {
            "recipient": ActionParamSpec(name="recipient", question="Who would you like to message?", required=True),
            "body": ActionParamSpec(name="body", question="What would you like to say?", required=True),
            "application": ActionParamSpec(name="application", question="Which application should we use to send?", required=True),
        }

    def clarify(self, prompt_fn: Callable) -> List[str]:
        super().clarify(prompt_fn)
        name = self.params["recipient"].value.strip()
        self.contact_info = contact_actions.clarify_contact_info(
            name=name,
            db=self.db,
            prompt_fn=prompt_fn,
            loop_until_found=True,
            prompt_for_alias=False,
        )

    def run(self):
        body = self.params["body"].value
        application = self.params["application"].value
        return ActionResult(
            reply_text=f"Sending message '{body}' to {self.contact_info.name} using {application}",
        )
