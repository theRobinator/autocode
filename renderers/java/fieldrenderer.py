import re


def render(field, owner):
    if field.has_prop('var'):
        field.remove_all_props('var')
    if field.type is None:
        raise Exception('Could not determine the type of the field %s' % field.type)

    field.add_prop('var', field.type.name)

    if field.const:
        field.remove_all_props('access')

    if field.description is None and len(field.props) == 0:
        result = ['/**', field.render_comment(), ' */']
    else:
        result = []

    if field.value is not None:
        value_str = ' = %s' % field.value
    else:
        value_str = ''

    if field.const:
            result.append('final %s %s%s;' % (field.type, field.name, value_str))
    else:
        if field.static:
            result.append('static %s $%s%s;' % (field.type, field.name, value_str))
        else:
            result.append('%s %s %s%s;' % (field.visibility, field.type, field.name, value_str))

    return "\n".join(result)
