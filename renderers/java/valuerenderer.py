import json
from autocode.language_utils.java import PRIMITIVE_MAPPING


def render(value):
    """
    Return a string representation of this value in the correct language.
    :param value: A literal value
    :return:
    """
    if type(value) == list:
        result = []
        if len(value) <= 0:
            raise Exception('Empty list. Cannot convert to java array')

        var_type = type(value[0])
        for i in value:
            if type(i) != var_type:
                raise Exception('All element in the list should be of the same type')
            result.append(render(i))

        if var_type.__name__ in PRIMITIVE_MAPPING:
            java_type = PRIMITIVE_MAPPING.get(var_type.__name__)
        else:
            java_type = var_type.__name__

        return 'new %s[]{%s};' % (java_type, ', '.join(result))
    elif type(value) == dict:
        result = []
        if len(value) <= 0:
            raise Exception('Empty python dict. Cannot convert to java dict')

        key, val = value.popitem()
        key_type = type(key)
        value_type = type(val)
        result.append('     put(%s,%s);' % (key, render(val)))
        for k, v in value.iteritems():
            if type(k) != key_type or type(v) != value_type:
                raise Exception('keys/values must be of the same type')
            result.append('     put(%s,%s);' % (k, render(v)))

        if key_type.__name__ in PRIMITIVE_MAPPING:
            java_key_type = PRIMITIVE_MAPPING.get(key_type.__name__)
        else:
            java_key_type = key_type.__name__

        if value_type.__name__ in PRIMITIVE_MAPPING:
            java_value_type = PRIMITIVE_MAPPING.get(key_type.__name__)
        else:
            java_value_type = key_type.__name__

        return 'new HashMap<%s,%s>(){{\n%s\n}};' % (java_key_type, java_value_type, '\n'.join(result))

    else:
        return json.dumps(value)