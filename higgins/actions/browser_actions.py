from typing import Dict

from higgins.actions import Action, ActionParamSpec, ActionResult


class BrowserAction(Action):

    def add_automations(self, automations: Dict) -> Dict:
        # self.browser = automations["browser"]
        # self.desktop = automations["desktop"]
        return automations


class OpenWebsite(BrowserAction):

    @classmethod
    def param_specs(cls):
        return {
            "website": ActionParamSpec(name="website", question="What is the URL?", required=True),
        }

    def run(self):
        return ActionResult(
            action_text=f"Opening website {self.params['website'].value}"
        )


class ClickLink(BrowserAction):

    @classmethod
    def param_specs(cls):
        return {
            "link_text": ActionParamSpec(name="link_text", question="Which link should we click on?", required=True),
        }

    def run(self):
        return ActionResult(
            action_text=f"Clicking link '{self.params['link_text'].value}'"
        )


class SearchOnWebsite(BrowserAction):

    @classmethod
    def param_specs(cls):
        return {
            "text": ActionParamSpec(name="text", question="What should we search for?", required=True),
            "filter": ActionParamSpec(name="filter", question="Would you like to apply any filters?", required=False),
        }

    def run(self):
        text = self.params['text'].value
        filter = self.params['filter'].value
        return ActionResult(
            action_text=f"Searching for '{text}' with filter '{filter}'"
        )


class SignOutOfWebsite(BrowserAction):

    @classmethod
    def param_specs(cls):
        return {
            "website": ActionParamSpec(name="website", question="Which website should we sign out of?", required=False),
        }

    def run(self):
        if self.params['website'].is_missing():
            self.params['website'].value = "[CURRENT_URL]"

        return ActionResult(
            action_text=f"Logging out of {self.params['website'].value}"
        )


class LogInToWebsite(BrowserAction):

    @classmethod
    def param_specs(cls):
        return {
            "website": ActionParamSpec(name="website", question="Which website should we log into?", required=False),
            "username": ActionParamSpec(name="username", question="What is your username?", required=True),
            "password": ActionParamSpec(name="password", question="What is your password?", required=True),
        }

    def run(self):
        if self.params['website'].is_missing():
            self.params['website'].value = "[CURRENT_URL]"
        username = self.params['username'].value
        password = "*" * len(self.params['password'].value)
        return ActionResult(
            action_text=f"Logging into {self.params['website'].value} with username: {username} and password: {password}"
        )
