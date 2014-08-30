from autocode.language_utils.php import PRIMITIVE_MAPPING, PYTHON_CONTAINER_MAPPING

def normalize_type(typename):
    """ Return a normalized version of a type name, free of any language-specific modifiers. """
    if typename.endswith('[]'):
        typename = typename[:-2]
    return typename


def render_python_primitive(type_name):
    """
    Return the name of the given Python type in the correct language.
    :param type_name: String|type: The type, e.g. 'str' or 'int'
    :return: The name of the type in the current language
    """
    if isinstance(type_name, type):
        type_name = type(type_name).__name__

    if type_name in PRIMITIVE_MAPPING:
        return PRIMITIVE_MAPPING[type_name]
    elif type_name in PYTHON_CONTAINER_MAPPING:
        return PYTHON_CONTAINER_MAPPING[type_name]
    else:
        return type_name


def render(typeobj, owner=None):
    """ Render what a type looks like in code.
        :param owner: The owner of the type.
    """
    if typeobj.subtype is None or typeobj.name != 'array':
        return typeobj.name
    else:
        # Guaranteed to be an array
        return '%s[]' % typeobj.subtype


def render_call(typeobj, owner=None, default_args=''):
    """ Render a call to this type (i.e. a constructor)
        :param typeobj: The type to render
        :param owner: The owner of the type
        :param default_args: Arguments passed to the call.
    """
    if type(default_args) == str:
        arg_str = default_args
    elif len(default_args) == 0:
        arg_str = ''
    elif type(default_args[0]) == Var:
        arg_str = ', '.join(i.name for i in default_args)
    else:
        arg_str = ', '.join(default_args)
    return 'new %s(%s)' % (normalize_type(typeobj.name), arg_str)

