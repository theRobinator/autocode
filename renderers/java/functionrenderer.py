
def render_call(func, owner=None, default_args=None):
    """ Return what a call to this function would look like """
    arguments = ', '.join(i.name for i in func.params)
    if owner is not None and func.static:
        return '%s.%s(%s)' % (owner.name, func.name, arguments)
    else:
        return '%s(%s)' % (func.name, arguments)


def render(func, owner):
    """ Return a string containing what this would look like in code. """
    param_string_parts = []
    for param in func.params:

        if param.type is None:
            raise Exception('Could not determine the type of the param %s' % param.name)

        if func.return_type is None and func.name != owner.name:
            raise Exception('Java function must have return type except default constructor')

        var_name = namerenderer.varify_name(param.name)
        if param.value is not None:
            var_name += '=' + param.value

        if param.description:
            desc_string = ' ' + param.description
        else:
            desc_string = ''

        func.add_prop('param', param.type.name, var_name + desc_string)
        param_string_parts.append('%s %s' % (param.type.name, var_name))

    param_string = ', '.join(param_string_parts)

    if func.return_type is not None:
        func.add_prop('return', func.return_type.name)

    result = ['/**', func.render_comment(), ' */']

    if func.name == owner.name:
        result.append("%s %s(%s)" % (func.visibility, func.name, param_string))
    elif func.static:
        result.append("%s static %s %s(%s) {" % (func.visibility, func.return_type, func.name, param_string))
    else:
        result.append("%s %s %s(%s) {" % (func.visibility, func.return_type, func.name, param_string))

    if len(func.body) > 0:
        # indent the function body
        result.append('    ' + "\n    ".join(func.body.split("\n")))

    result.append('}')
    return "\n".join(result)
