def render_call(func, owner=None, default_args=None):
    """ Return what a call to this function would look like """
    arguments = ', '.join(i.name for i in func.params)
    if owner is not None and func.static:
        return '%s.%s(%s)' % (owner.name, func.name, arguments)
    else:
        return '%s(%s)' % (func.name, arguments)


def render(func, owner):
    """ Return a string containing what this would look like in code. """
    if func.visibility != 'public':
        func.add_prop(func.visibility)

    for param in func.params:
        func.add_prop('param', param.type, param.name)
    if func.return_type is not None:
        func.add_prop('return', func.return_type)

    result = ['/**', func.render_comment(), ' */']

    param_string = ', '.join(x.name for x in func.params)

    if owner.name is None or owner.name == '':
        result.append('%s = function(%s) {' % (func.name, param_string))
    elif func.static:
        result.append('%s.%s = function(%s) {' % (owner.name, func.name, param_string))
    else:
        result.append('%s.prototype.%s = function(%s) {' % (owner.name, func.name, param_string))

    if len(func.body) > 0:
        # indent the function body
        result.append('    ' + "\n    ".join(func.body.split("\n")))

    result.append('};')
    return "\n".join(result)
