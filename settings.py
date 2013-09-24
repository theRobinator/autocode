"""
    The settings file. Change settings here to modify how autocode acts.
"""

# The language that will be rendered. This is one of the package names in the renderers/ directory,
# e.g. 'closure' or 'php'.
language = 'closure'


# Whether Type objects should compile themselves by default. If true, Type objects will be able to
# modify their parents on compilation. This is powerful, but can cause problems when parsing code
# from source if you're doing specialized tasks.
compile_types = True
