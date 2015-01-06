def render(enum, owner):
    if enum.value_type is None:
        raise Exception('Enums must have type')

    if (enum.description is None or enum.description == '') and len(enum.props) == 0:
        result = []
    else:
        result = ['/**', enum.render_comment(), ' */']

    result.append("%s enum %s {" % (enum.visibility, enum.name))
    for key, value in sorted(enum.values):
        if value is None:
            result.append('    ' + "%s," % key)
        else:
            result.append('    ' + "%s(%s)," % (key, value))
    result.append('}')
    return "\n".join(result)