from autocode.renderers import propertyrenderer

class Property(object):
    """ A Property appears on anything that is definable. In code, it appears
        as a doctag. A property always has a name, but then may also have extended
        information. The full form usually looks like:
        @name modifier ident description
    """

    #: The property's name. This will be the doctag in most languages.
    name = ''

    #: The modifier. This is the second thing to appear in most languages, and the type of params.
    modifier = ''

    #: The identifier for the tag. This is the third thing to appear, and the variable name in params.
    ident = ''

    #: The description for the tag. This can be any length of text used to describe the property.
    description = ''

    def __init__(self, name, modifier='', ident='', description=''):
        self.name = name
        self.modifier = modifier
        self.ident = ident
        self.description = description

    def __str__(self):
        return propertyrenderer.render(self)

    def __eq__(self, other):
        return self.name == other.name and \
            self.modifier == other.modifier and \
            self.ident == other.ident and \
            self.description == other.description
