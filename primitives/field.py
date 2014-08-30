from autocode.primitives.definable import Definable
from autocode.primitives.document import Document
from autocode.primitives.autocode_type import Type
from autocode.renderers import fieldrenderer
from autocode import settings


class Field(Definable):
    """ A field is defined in a document or class with properties of its own. """

    #: This field's type.
    type = None

    #: Whether this field is static.
    static = False

    #: Whether this field is a const.
    const = False

    #: This field's default value.
    value = None

    #: Whether this value can be set to null.
    nullable = True

    def __init__(self, name, ctype, value=None, static=False, visibility='public', props=None, nullable=True, const=False):
        if type(ctype) == str:
            ctype = Type.get(ctype)

        super(Field, self).__init__(name, props=props, visibility=visibility)
        self.type = ctype
        self.static = static
        self.value = value
        self.nullable = nullable
        self.const = const

    def compile(self, owner, compile_types=settings.compile_types):
        """ Perform actions to ready whatever this is for rendering """
        if self.type is not None:
            if isinstance(owner, Document):
                # This is a top level field, so it must be static
                if compile_types:
                    self.type.compile(self)
                self.static = True
            elif compile_types:
                self.type.compile(self, owner)

    def render(self, owner):
        """ Return a string containing what this would look like in code. """
        return fieldrenderer.render(self, owner)
