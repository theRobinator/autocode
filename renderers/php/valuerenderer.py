import json


def render(value):
    """
    Return a string representation of this value in the correct language.
    :param value: A literal value
    :return:
    """
    if type(value) == list:
        result = []
        for i in value:
            result.append(render(i))
        return 'array(%s)' % ', '.join(result)

    elif type(value) == dict:
        result = []
        for k, v in value.iteritems():
            result.append('%s => %s' % (k, render(v)))
        return 'array(%s)' % ', '.join(result)

    else:
        return json.dumps(value)
