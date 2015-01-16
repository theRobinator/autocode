from autocode import settings


def render(field, owner):
    if field.type is None:
        raise Exception('Could not determine the type of the field %s' % field.type)

    comments = field.render_comment()
    if comments == " *" and settings.get_render_desctiptionless_doctage() is False:
        result = []
    else:
        result = ['/**', comments, ' */']

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
