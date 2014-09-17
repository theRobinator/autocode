def render(enum, owner):
    if enum.value_type is None:
        raise Exception('Enums must have types in closure.')
    enum.add_prop('enum', enum.value_type.name)

    if enum.visibility != 'public':
        enum.add_prop(enum.visibility)

    result = ['/**', enum.render_comment(), ' */']
    result.append('%s = {' % enum.name)
    result.append('    ' + ",\n    ".join('%s: %s' % i for i in sorted(enum.values)))
    result.append('};')
    return "\n".join(result)
