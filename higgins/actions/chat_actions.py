from higgins.actions import Action, ActionResult, ActionParamSpec


class DisplayText(Action):
    """Display text to console."""

    @classmethod
    def param_specs(cls):
        return {
            "text": ActionParamSpec(name="text", question="What text to display?", required=True),
            "data": ActionParamSpec(name="data"),
            "reply_handler_classname": ActionParamSpec(name="reply_handler_classname"),
        }

    def run(self):
        return ActionResult(
            reply_text=self.params['text'].value,
            data=self.params["data"].value,
            reply_handler_classname=self.params["reply_handler_classname"].value,
        )
