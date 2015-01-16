from autocode.renderers.java import namerenderer
from autocode import settings

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

    if func.return_type is None and func.name != owner.name:
            raise Exception('All Java functions other than constructors must have return types"')

    for param in func.params:
        if param.type is None:
            raise Exception('Could not determine the type of the param %s' % param.name)

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

    if func.return_type is not None and not func.has_prop('return'):
        func.add_prop('return')

    comments = func.render_comment()
    if comments == " *" and settings.get_render_desctiptionless_doctage() is False:
        result = []
    else:
        result = ['/**', comments, ' */']

    if len(func.annotations) > 0:
        result.extend(x.render(func) for x in func.annotations)

    if func.name == owner.name:
        result.append("%s %s(%s) {" % (func.visibility, func.name, param_string))
    elif func.static:
        result.append("%s static %s %s(%s) {" % (func.visibility, func.return_type, func.name, param_string))
    else:
        result.append("%s %s %s(%s) {" % (func.visibility, func.return_type, func.name, param_string))

    if len(func.body) > 0:
        # indent the function body
        result.append('    ' + "\n    ".join(func.body.split("\n")))

    result.append('}')
    return "\n".join(result)
