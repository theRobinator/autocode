from autocode import settings
from autocode import utils

def render(prop):
    """ Render a single property. """
    result = ['@%s' % prop.name]
    if prop.modifier != '':
        result.append('{%s}' % prop.modifier)
    if prop.ident != '':
        result.append(prop.ident)
    if prop.description != '':
        result.append(prop.description)
    return ' '.join(result)

def render_comment(props, description=''):
    """ Render properties in comment form.
        :param props: A list of Property objects that appear in the comment.
        :param description: The description to appear above the properties.
    """
    if description is None and len(props) == 0:
        return utils.EMPTY_COMMENT

    useful_props = []
    # this block checks if there are any useful docs to render
    if settings.get_redundant_doctag_setting() is False:
        for prop in props:
            if prop.description != '' or prop.name not in utils.REDUNDANT_DOCTAGS:
                useful_props.append(prop)
    else:
        useful_props = props

    result = []
    if description != '' and description is not None:
        result.append(' * ' + description.replace("\n", "\n * "))
    for prop in useful_props:
        if prop.name == 'inheritDoc':
            return ' * @inheritDoc'
        result.append(' * ' + render(prop))

    return "\n".join(result)
