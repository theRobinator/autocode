"""
    The settings file. Change settings here to modify how autocode acts.
"""
from autocode import languages


class SettingsManager(object):
    # The language that will be rendered. This is one of the package names in the renderers/ directory,
    # e.g. 'closure' or 'php'.
    language = languages.CLOSURE

    # Whether or not to render doctags that are already defined in method or field signatures, such as "@access" or
    # "@return". When this is False, these tags will not be rendered unless a description is added to them.
    render_descriptionless_doctags = True


def get_language():
    return SettingsManager.language


def set_language(language):
    """ Set the language that's used when rendering.
    :param language: One of the language constants
    """
    SettingsManager.language = language

def set_render_descriptionless_doctage(value):
    if value not in [True, False]:
        raise Exception("Invalid value provided to set render_descriptionless_doctags")
    SettingsManager.render_descriptionless_doctags = value

def get_render_desctiptionless_doctage():
    return SettingsManager.render_descriptionless_doctags


# Whether Type objects should compile themselves by default. If true, Type objects will be able to
# modify their parents on compilation. This is powerful, but can cause problems when parsing code
# from source if you're doing specialized tasks.
compile_types = True
