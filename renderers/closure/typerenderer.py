

def normalize_type(typename):
    """ Return a normalized version of a type name, free of any language-specific modifiers. """
    if typename.startswith('...'):
        typename = typename[3:]
    if typename[0] == '!' or typename[0] == '?':
        typename = typename[1:]
    if typename[-1] == '?' or typename[-1] == '=':
        typename = typename[:-1]
    return typename


def render(typeobj, owner=None):
    """ Render what a type looks like in code.
        :param owner: The owner of the type.
    """
    return typeobj.name


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
    elif type(default_args[0]) == ClosureVar:
        arg_str = ', '.join(i.name for i in default_args)
    else:
        arg_str = ', '.join(default_args)
    return 'new %s(%s)' % (normalize_type(typeobj.name), arg_str)
