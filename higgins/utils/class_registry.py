import os
from typing import Dict, List, Type

from higgins.nlp.phrase_matcher import PhraseMatcher


def load_classes_from_modules(
    dir_name: str, file_suffix: str, class_type: Type
) -> Dict:
    """Loop through sub directories and load all the packages
    and return them as a dictionary"""
    class_map = {}
    file_list = os.listdir(os.path.join(os.getcwd(), dir_name))
    for file_name in file_list:
        full_path = os.path.join(os.path.abspath(dir_name), file_name)
        rel_path = os.path.join(dir_name, file_name)
        if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, "__init__.py")):
            class_map.update(load_classes_from_modules(rel_path))
        elif full_path.endswith(file_suffix) and file_name != "__init__.py":
            module_name = os.path.splitext(file_name)[0]
            module = __import__(
                f"{dir_name.replace(os.sep, '.')}.{module_name}", fromlist = ["*"])
            for _, t_value in module.__dict__.items():
                try:
                    if issubclass(t_value, class_type):
                        class_name = t_value.__name__
                        class_map[class_name] = t_value
                except:
                    # Some members of the module aren't classes. Ignore them.
                    pass
    return class_map


def load_class_by_name(class_name, class_map):
    if class_name not in class_map:
        raise Exception(f"Class: {class_name} not found!")
    return class_map[class_name]


def load_class_phrase_map_from_modules(
    dir_name: str, file_suffix: str, class_type: Type
) -> Dict[PhraseMatcher, Type]:
    """Loop through sub directories and load all the packages
    and return them as a dictionary"""
    phrase_map = {}
    file_list = os.listdir(os.path.join(os.getcwd(), dir_name))
    for file_name in file_list:
        full_path = os.path.join(os.path.abspath(dir_name), file_name)
        rel_path = os.path.join(dir_name, file_name)
        if os.path.isdir(full_path) and \
            os.path.exists(os.path.join(full_path, "__init__.py")):
            phrase_map.update(load_class_phrase_map_from_modules(rel_path))
        elif full_path.endswith(file_suffix) and file_name != "__init__.py":
            module_name = os.path.splitext(file_name)[0]
            module = __import__(
                f"{dir_name.replace(os.sep, '.')}.{module_name}",
                fromlist = ["*"])
            for _, t_value in module.__dict__.items():
                try:
                    if issubclass(t_value, class_type):
                        for phrase in t_value.phrases():
                            # TODO(hari): Validate the phrases to make sure
                            # they don't use invalid param names and types
                            phrase_matcher = PhraseMatcher(phrase)
                            phrase_map[phrase_matcher] = t_value
                except:
                    # Some members of the module aren't classes. Ignore them.
                    pass
    return phrase_map


def find_matching_classes(phrase: str, phrase_map: Dict[str, PhraseMatcher]) -> List[Type]:
    classes = []
    for phrase_matcher, class_type in phrase_map.items():
        status, params = phrase_matcher.match(phrase)
        if status:
            classes.append((class_type, params))
    return classes
