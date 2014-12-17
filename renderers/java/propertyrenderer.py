

def render(prop):
    """ Render a single property. """
    result = ['@%s' % prop.name]
    if prop.modifier != '':
        result.append(prop.modifier)
    if prop.ident != '':
        result.append(prop.ident)
    if prop.description != '':
        result.append(prop.description)
    return ' '.join(result)

def render_comment(props, description=None):
    """ Render properties in comment form.
        :param props: A list of Property objects that appear in the comment.
        :param description: The description to appear above the properties.
    """
    if description is None and len(props) == 0:
        return ' *'

    result = []
    if description != '' and description is not None:
        result.append(' * ' + description.replace("\n", "\n * "))
    for prop in props:
        result.append(' * ' + render(prop))

    result = "\n".join(result)
    if result == '':
        return ' *'
    else:
        return result
