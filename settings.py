"""
    The settings file. Change settings here to modify how autocode acts.
"""
from autocode import languages


class SettingsManager(object):
    # The language that will be rendered. This is one of the package names in the renderers/ directory,
    # e.g. 'closure' or 'php'.
    language = languages.CLOSURE


def get_language():
    return SettingsManager.language


def set_language(language):
    """ Set the language that's used when rendering.
    :param language: One of the language constants
    """
    SettingsManager.language = language

# Whether Type objects should compile themselves by default. If true, Type objects will be able to
# modify their parents on compilation. This is powerful, but can cause problems when parsing code
# from source if you're doing specialized tasks.
compile_types = True
