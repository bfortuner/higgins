import importlib
import inspect


def load_class_by_name(name: str):
    # name: my_package.my_module.LaunchAction
    tree = name.split(".")
    module = importlib.import_module(".".join(tree[:-1]))
    cls = getattr(module, tree[-1])
    return cls


def get_class_init_args(cls):
    sig = inspect.signature(cls.__init__)
    exclude_params = ["self", "kwarg"]
    return [k for k in sig.parameters.keys() if k not in exclude_params]


def get_fully_qualified_class_name(cls):
    return ".".join([cls.__module__, cls.__name__])


def add_automation_to_action_params(
    action_cls, action_params, desktop=None, browser=None
):
    if "browser" in action_cls.automations():
        action_params["browser"] = browser
    if "desktop" in action_cls.automations():
        action_params["desktop"] = desktop


def action_to_dict(action_cls, action_params):
    exclude_params = ["desktop", "browser"]
    params = {
        k: v for k, v in action_params.items() if k not in exclude_params
    }
    class_name = ".".join([action_cls.__module__, action_cls.__name__])
    return {
        "class": class_name,
        "params": params,
    }


def dict_to_action(dct):
    dct["class"] = load_class_by_name(dct["class"])
    return dct
