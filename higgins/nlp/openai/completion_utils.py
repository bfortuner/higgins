import re
from typing import Dict, List, Tuple

from higgins import const


def extract_params_from_string(string: str) -> Dict:
    """Convert completion string to dictionary of params.

    Args:
        string: Raw text version of action chain

    Returns:
        Dict: Extracted parameters

    Example:
        string: to=>mom ### body=>I Love her ### application=>???
        out: {"recipient": "mom", "body":"I love her", "application": None}
    """
    params = string.strip().split("###")
    out = {}
    for param in params:
        argument, value = param.strip().split("=>")
        out[argument.strip()] = value.strip()
    return out


def convert_action_chain_to_string(action_chain: List[Dict]) -> str:
    """Convert dictionary of params to completion string.

    Args:
        params (Dict): Dictionary of completion params

    Returns:
        str: Completion string

    Example:
        params: [
            {'action': 'ActionWithParams', 'params': {'recipient': 'mom', 'body': 'I love her'}},
            {'action': 'ActionMissingParams', 'params': {'application': '???'}},
            {'action': 'ActionNoParams', 'params': {}},
        ]
        returns:
        `ActionWithParams` PARAMS to=>mom ### body=>I love her -> `ActionMissingParams` PARAMS application=??? -> `ActionNoParams` <<END>>

    """
    action_strings = []
    for action in action_chain:
        action_str = [f"`{action['action']}`"]
        if action['params']:
            action_str.append("PARAMS")
            action_str.append(" ### ".join([f"{name}=>{value}" for name, value in action['params'].items()]))
        action_strings.append(" ".join(action_str))
    action_strings = " -> ".join(action_strings)
    action_strings += " <<END>>"
    return action_strings


def convert_string_to_action_chain(string: str) -> List[Dict]:
    """Convert completion string to action chain.

    Args:
        string (str): Completion string

    Raises:
        Exception: If command doesn't matched expected format.

    Returns:
        List[Dict]: List of actions and parameters
    """
    if const.DEBUG_MODE:
        print(f"Answer: {string}")

    PARAMS_REGEX = r"`([a-zA-Z]+)`\sPARAMS\s(.*)"
    NO_PARAMS_REGEX = r"`([a-zA-Z]+)`"
    cmds = string.split(" -> ")
    actions = []
    for cmd in cmds:
        cmd = cmd.strip()
        match_with_params = re.match(PARAMS_REGEX, cmd)
        if match_with_params and len(match_with_params.groups()) == 2:
            class_name, param_string = match_with_params.groups()
            actions.append({
                "action": class_name,
                "params": extract_params_from_string(param_string)
            })
            continue

        match_no_params = re.match(NO_PARAMS_REGEX, cmd)
        if match_no_params and len(match_no_params.groups()) == 1:
            print(match_no_params)
            class_name = match_no_params.groups()[0]
            print(class_name)
            actions.append({"action": class_name, "params": None})
        else:
            raise Exception(
                f"Unabled to parse command: {cmd}, from answer: {string}"
            )
    if const.DEBUG_MODE:
        print(f"Actions: {actions}")
    return actions


def build_completion_prompt(
    question: str,
    action_chains: List[Dict],
    task_description: str = None,
) -> str:
    prompt = ""
    if task_description is not None:
        prompt += f"{task_description}\n"

    for action in action_chains:
        completion = convert_action_chain_to_string(action["actions"])
        prompt += f"\nQ: {action['query']}"
        prompt += f"\nA: {completion}"

    prompt += "\nQ: {question}".format(question=question)
    prompt += "\nA:"
    return prompt


if __name__ == "__main__":
    expected_action_chain = [
        {'action': 'ActionWithParams', 'params': {'recipient': 'mom', 'body': 'I love her'}},
        {'action': 'ActionMissingParams', 'params': {'application': '???'}},
        {'action': 'ActionNoParams', 'params': None},
    ]
    expected_chain_str = "`ActionWithParams` PARAMS to=>mom ### body=>I love her -> `ActionMissingParams` PARAMS application=>??? -> `ActionNoParams` <<END>>"
    chain_str = convert_action_chain_to_string(expected_action_chain)
    print(expected_chain_str)
    print(chain_str)

    assert chain_str == expected_chain_str

    chain = convert_string_to_action_chain(chain_str)
    print(expected_action_chain)
    print(chain)

    assert chain == expected_action_chain
