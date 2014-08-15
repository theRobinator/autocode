import json

def render(value):
    """
    Return a string representation of this value in the correct language.
    :param value: A literal value
    :return:
    """
    return json.dumps(value)
