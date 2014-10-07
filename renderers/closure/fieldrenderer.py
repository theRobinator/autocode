def render(field, owner):
    if field.visibility != 'public':
        field.add_prop(field.visibility)

    if field.has_prop('type'):
        field.remove_all_props('type')
    if field.type is not None:
        if field.nullable:
            field.add_prop('type', field.type.name)
        else:
            field.add_prop('type', '!' + field.type.name)

    result = ['/**', field.render_comment(), ' */']

    if field.value is not None:
        value_str = ' = %s' % field.value
    else:
        value_str = ''

    if owner.name is None or owner.name == '':
        result.append('%s%s;' % (field.name, value_str))
    elif field.static:
        if field.name.startswith(owner.name + '.'):
            result.append('%s%s;' % (field.name, value_str))
        else:
            result.append('%s.%s%s;' % (owner.name, field.name, value_str))
    else:
        result.append('%s.prototype.%s%s;' % (owner.name, field.name, value_str))

    return "\n".join(result)
