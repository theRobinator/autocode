from autocode.primitives.cls import Class
from autocode.primitives.autocode_type import Type
from autocode.renderers import enumrenderer
from autocode import settings


class Enum(Class):
    """ An enum, with several values. """

    #: This enum's values.
    values = None

    #: The type of the enum's values. Note that this only makes sense in some languages.
    value_type = None


    def __init__(self, name, value_type=None, visibility='public', props=None, description=None, implements=None, params=None):
        if type(value_type) == str:
            value_type = Type.get(value_type)
        super(Enum, self).__init__(name, props=props, visibility=visibility, description=description, implements=implements, params=params)
        self.value_type = value_type
        self.values = []

    def add_value(self, key, value=None):
        """ Add a value to this enum. """
        if self.has_key(key) is False:
            self.values.append((key, value))

    def remove_value(self, key, value=None):
        """ Remove a value from this enum. """
        self.values.remove((key, value))

    def has_key(self, key):
        for k, v in self.values:
            if k == key:
                return True
        return False

    def compile(self, owner, compile_types=settings.compile_types):
        """ Perform actions to ready whatever this is for rendering """
        if compile_types and self.value_type is not None:
            self.value_type.compile(self)

    def render(self, owner):
        """ Return a string containing what this would look like in code. """
        return enumrenderer.render(self, owner)
