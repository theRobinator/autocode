import re


def render(field, owner):
    if field.type is None:
        raise Exception('Could not determine the type of the field %s' % field.type)

    # add docs only if the field has a description or property
    if (field.description is None or field.description == '') and len(field.props) == 0:
        result = []
    else:
        result = ['/**', field.render_comment(), ' */']

    if field.value is not None:
        value_str = ' = %s' % field.value
    else:
        value_str = ''

    if field.const:
            result.append('%s final %s %s%s;' % (field.visibility, field.type, field.name, value_str))
    else:
        if field.static:
            result.append('%s static %s $%s%s;' % (field.visibility, field.type, field.name, value_str))
        else:
            result.append('%s %s %s%s;' % (field.visibility, field.type, field.name, value_str))

    return "\n".join(result)
