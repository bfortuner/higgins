import re
from typing import Dict, List, Tuple

from higgins.const import AUTOMATION_PARAMS
from higgins.actions import ActionBase, ActionChain, ActionChainStep
from higgins.actions import action_utils
from higgins.nlp.openai import navigation


def parse_answer_to_actions(answer: str) -> Tuple[str, str]:
    # HACK: Only supports single parameter Actions
    # TODO: These Regex still capture badly formed strings
    PARAMS_REGEX = r"([a-zA-Z]+)+\s+`(.*)`"
    NO_PARAMS_REGEX = r"([a-zA-Z]+)"
    print(f"Parsing answer: {answer}")
    cmds = answer.split(" -> ")
    print(f"Commands: {cmds}")
    actions = []
    for cmd in cmds:
        cmd = cmd.strip()
        match_with_params = re.match(PARAMS_REGEX, cmd)
        if match_with_params and len(match_with_params.groups()) == 2:
            print("found match with params")
            class_name, param = match_with_params.groups()
            actions.append((class_name, param))
            continue

        match_no_params = re.match(NO_PARAMS_REGEX, cmd)
        if match_no_params and len(match_no_params.groups()) == 1:
            print("found match with no params")
            class_name = match_no_params.group(0)
            actions.append((class_name, None))
        else:
            raise Exception(
                f"Unabled to parse command: {cmd}, from answer: {answer}"
            )
    return actions


def convert_actions_to_chain(
    cmd: str,
    actions: List[Tuple[str, str]],
    action_classes: Dict[str, ActionBase],
) -> ActionChain:
    # HACK: Provide another way to alias classes.
    action_steps = []
    for class_name, param in actions:
        action_class = action_classes[class_name]
        class_path = action_utils.get_fully_qualified_class_name(action_class)
        param_names = action_utils.get_class_init_args(action_class)
        print(action_class, param_names)
        step = ActionChainStep(
            class_path=class_path,
            # HACK: we only support 1 param for Action
            params={name: param for name in param_names if name not in AUTOMATION_PARAMS}
        )
        action_steps.append(step)

    return ActionChain(
        name=cmd,
        phrases=[cmd],
        steps=action_steps,
    )


def infer_action_chain(cmd: str, action_classes: Dict[str, ActionBase]) -> ActionChain:
    # action_classes["ChangeURL"] = action_classes["ChangeURL"]
    answer = navigation.ask_web_navigation_model(cmd, engine="davinci")
    actions = parse_answer_to_actions(answer)
    for class_name, _ in actions:
        if class_name not in action_classes.keys():
            raise Exception(f"Action: {class_name} not found for answer: {answer}")
    chain = convert_actions_to_chain(cmd, actions, action_classes)
    return chain
