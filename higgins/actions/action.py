from __future__ import annotations  # Required for using current class in a type annotation

from dataclasses import dataclass, asdict
import json
from typing import Any, Callable, Dict, List

from higgins.actions import action_utils


@dataclass
class ActionResult:
    """Stores the status and error of an executed action.

    Args:
        status: succeeded or failed
        error: error message if failed
        action_text: text about actions Higgins is performing (e.g. "opening browser")
        reply_text: text to respond to the user (e.g. "I don't understand")
        data: data returned by Action
        reply_handler_classname: Name of IntentParser to handle follow-up actions
    """
    status: str = "succeeded"  # succeeded, failed
    error: str = None  # exception message
    action_text: str = None  # Can be a List[str] for multi-line chat
    reply_text: str = None  # Can be a List[str] for multi-line chat
    data: Dict = None
    reply_handler_classname: str = None


@dataclass
class ActionParamSpec:
    """Incorporates metadata about an action class parameter.

    If it's required, what the clarifying question is, and it's name. This
    is useful for validation and prompt generation.
    """
    name: str
    question: str = None
    valid_types: List = None
    required: bool = False

    def is_valid(self, value: Any) -> bool:
        """Return True if input is a valid value(s) for this parameter."""
        valid = True
        if self.valid_types is not None:
            valid = type(value) in self.valid_types
        return valid


@dataclass
class ActionParam:
    """Incorporates metadata about an action class parameter.

    If it's required, what the clarifying question is, and it's name. This
    is useful for validation and prompt generation.
    """
    value: Any
    spec: ActionParamSpec

    def is_valid(self) -> bool:
        """Return True if input is a valid value(s) for this parameter."""
        return self.spec.is_valid(self.value)

    def is_missing(self) -> bool:
        return self.value is None or self.value == "???"


class Action:
    """Base class for all Actions.

    Actions know how to:
    - Parse intent and parameters from raw text
    - Load sub-actions needed to run
    - Run and execute the sequence of actions
    - Prompt the user with clarifying questions to finalize parameters.
    """

    def __init__(self, params: Dict = None):
        self.params = params or {}

    @classmethod
    def param_specs(cls) -> Dict[str, ActionParamSpec]:
        """Dictionary of parameters needed to instantiate this Action."""
        return {}

    @classmethod
    def from_params(cls, params: Dict[str, ActionParam]) -> Action:
        """Initialize Action given dictionary of `ActionParam` objects. 

        No text parsing required. Allows other Actions to call this action directly.
        """
        return cls(params=params)

    @classmethod
    def from_dict(cls, dct: Dict[str, Any]) -> Action:
        """Initialize an Action given a dictionary of parameter values.

        Allows us to load serialized actions.
        """
        params = {}
        for param_name, param_value in dct.items():
            params[param_name] = ActionParam(
                value=param_value,
                spec=cls.param_specs()[param_name]
            )
        return cls(params=params)

    def to_dict(self):
        """Serialize to dictionary. Subclasses can override this
        method to add additional metadata to their dictionary.
        """
        return {
            "name": self.name,
            "params": [asdict(p) for _, p in self.params.items()]
        }

    @property
    def name(self):
        return type(self).__name__

    @property
    def class_path(self):
        cls = type(self)
        return action_utils.get_fully_qualified_class_name(cls)

    def add_automations(self, automations: Dict) -> Dict:
        """Add automation instances, init new ones, and return updated dict.
        Automations are lazy loaded, due to possible initialization costs.
        New automations are added to the dictionary and returned.
        """
        return automations

    def clarify(self, prompt_fn: Callable):
        """Populate missing action parameters.

        Params:
            prompt_fn: Function which prompts the user (prints question to console)

        Either query using a database or ask the user if some parameters
        are missing. The database is updated with any new information.
        """
        for param in self.params.values():
            if param.is_missing():
                if param.spec.required:
                    param.value = prompt_fn(f"{param.spec.question} ")
                else:
                    param.value = None

    def run(self) -> ActionResult:
        """Execute the action.

        Currently requires that all required parameters are provided. The caller
        is responsible for asking clarifying questions to prompt the user for more info.
        """
        raise NotImplementedError("Needs to be implemented by the derived class")

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=2)
