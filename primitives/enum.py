from autocode.primitives.definable import Definable
from autocode.primitives.type import Type
from autocode.renderers import enumrenderer
from autocode import settings


class Enum(Definable):
    """ An enum, with several values. """

    #: This enum's values.
    values = None

    #: The type of the enum's values. Note that this only makes sense in some languages.
    value_type = None

    def __init__(self, name, value_type=None, visibility='public', props=None):
        if type(value_type) == str:
            value_type = Type.get(value_type)
        super(Enum, self).__init__(name, props=props, visibility=visibility)
        self.value_type = value_type

        self.provides.add(name)
        self.values = []

    def add_value(self, key, value=None):
        """ Add a value to this enum. """
        self.values.append((key, value))

    def remove_value(self, key, value=None):
        """ Remove a value from this enum. """
        self.values.remove((key, value))

    def compile(self, owner, compile_types=settings.compile_types):
        """ Perform actions to ready whatever this is for rendering """
        if compile_types and self.value_type is not None:
            self.value_type.compile(self)

    def render(self, owner):
        """ Return a string containing what this would look like in code. """
        return enumrenderer.render(self, owner)
