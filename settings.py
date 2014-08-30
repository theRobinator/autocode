"""
    The settings file. Change settings here to modify how autocode acts.
"""

class SettingsManager(object):

    # The language that will be rendered. This is one of the package names in the renderers/ directory,
    # e.g. 'closure' or 'php'.
    language = 'php'




def get_language():
    return SettingsManager.language

language = get_language()

# Whether Type objects should compile themselves by default. If true, Type objects will be able to
# modify their parents on compilation. This is powerful, but can cause problems when parsing code
# from source if you're doing specialized tasks.
compile_types = True
