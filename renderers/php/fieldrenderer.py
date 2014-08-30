import re


def render(field, owner):
    if field.has_prop('var'):
        field.remove_all_props('var')
    if field.type is not None:
        if field.nullable and not '[]' in field.type.name and not re.search('\|?null\|?', field.type.name):
            field.add_prop('var', field.type.name + '|null')
        else:
            field.add_prop('var', field.type.name)


    if field.const:
        field.remove_all_props('access')

    result = ['/**', field.render_comment(), ' */']

    if field.value is not None:
        value_str = ' = %s' % field.value
    else:
        value_str = ''

    if field.const:
        result.append('const %s%s;' % (field.name, value_str))
    else:
        if field.static:
            result.append('%s static $%s%s;' % (field.visibility, field.name, value_str))
        else:
            result.append('%s $%s%s;' % (field.visibility, field.name, value_str))

    return "\n".join(result)
