def render(enum, owner):
    # PHP doesn't have enums! D:
    # Instead we can use an abstract class with constant values, ugh

    result = ['/**', ' */']
    result.append('abstract class %s {' % enum.name)
    result.append('    ' + "\n    ".join('const %s = %s;' % i for i in sorted(enum.values)))
    result.append('}')
    return "\n".join(result)
