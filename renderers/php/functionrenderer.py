from autocode.renderers.php import namerenderer
from autocode.language_utils.php import PRIMITIVE_TYPES


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
        var_name = namerenderer.varify_name(param.name)
        if param.value is not None:
            var_name += '=' + param.value

        if param.description:
            desc_string = ' ' + param.description
        else:
            desc_string = ''
        if param.type is None:
            func.add_prop('param', var_name + desc_string)
        else:
            func.add_prop('param', param.type.name, var_name + desc_string)

        if param.type is None or param.type.name in PRIMITIVE_TYPES:
            param_string_parts.append(var_name)
        elif param.type.name.endswith('[]'):
            param_string_parts.append('array %s' % var_name)
        else:
            param_string_parts.append('%s %s' % (param.type.name, var_name))

    param_string = ', '.join(param_string_parts)

    if func.return_type is not None:
        func.add_prop('return', func.return_type.name)

    result = ['/**', func.render_comment(), ' */']

    if func.static:
        result.append("%s static function %s(%s)\n{" % (func.visibility, func.name, param_string))
    else:
        result.append("%s function %s(%s)\n{" % (func.visibility, func.name, param_string))

    if len(func.body) > 0:
        # indent the function body
        result.append('    ' + "\n    ".join(func.body.split("\n")))

    result.append('}')
    return "\n".join(result)
