from autocode.primitives.nameable import Nameable
from autocode.renderers import typerenderer


class Type(Nameable):
    """ A type is an object type that variables and fields can have, and can be
        instantiated using constructors.
    """

    #: The singleton registry for types
    _registry = {}

    def __init__(self, name):
        super(Type, self).__init__(name)

    def compile(self, owner, parent_class=None):
        """ Perform actions to ready whatever owns this for rendering """
        pass

    def render_call(self, owner=None, default_args=''):
        """ Return what a call to this type would look like """
        return typerenderer.render_call(self, owner, default_args)

    def render(self, owner):
        """ Return a string containing what this would look like in code. """
        return typerenderer.render(self, owner)

    @classmethod
    def add_type(cls, type):
        """ Add a type class pointer to the registry. """
        if type.name in cls._registry:
            raise Error("Type %s is already defined." % type.name)
        cls._registry[type.name] = type

    @classmethod
    def get(cls, name):
        """ Get the singleton instance of a named type. """
        if name in cls._registry:
            return cls._registry[name](name)
        else:
            normal_name = typerenderer.normalize_type(name)
            if normal_name in cls._registry:
                instance = cls._registry[normal_name](name)
                instance.name = name
                return instance
            else:
                instance = Type(name)
                cls._registry[normal_name] = Type
                return instance
