def render(enum, owner):
    if enum.value_type is None:
        raise Exception('Enums must have type')

    enum.add_prop('enum', enum.value_type.name)
    result = []
    result.append("%s enum %s {" % (enum.visibility, enum.name))
    for key, value in sorted(enum.values):
        if value is None:
            result.append('    ' + "%s," % key)
        else:
            result.append('    ' + "%s(%s)," % (key, value))
    result.append('}')
    return "\n".join(result)
