def render(annotation, owner):

    result = '@' + annotation.name
    if len(annotation.args) > 0:
        result += '(' + ','.join(annotation.args) + ')'

    return result