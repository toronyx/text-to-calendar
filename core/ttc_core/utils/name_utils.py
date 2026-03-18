import re


def to_snake_case(s):  # TODO 18-Mar-2026 test this function
    s = re.sub(r"[\-\s]+", "_", s)  # replace spaces/dashes
    s = re.sub(r"(?<!^)(?=[A-Z])", "_", s)  # split CamelCase
    return s.lower()
