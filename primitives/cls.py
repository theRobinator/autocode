from autocode.primitives.definable import Definable
from autocode.primitives.autocode_type import Type
from autocode.primitives.var import Var
from autocode.renderers import classrenderer
from autocode import settings
from autocode import utils


class Class(Definable):
    """ A class that appears in a document. """

    #: The type that this class extends.
    extends = None

    #: The type or types that this class implements (a list)
    implements = None

    #: This class's fields
    fields = None

    #: This class's methods
    methods = None

    #: The params for this class's constructor
    params = None

    #: The body of this class's constructor
    constructor = None

    #: This class's type
    type = None

    def __init__(self, full_name, params=None, extends=None, implements=None, constructor_body=None, visibility='public', props=None):
        super(Class, self).__init__(full_name, props=props, visibility=visibility)

        self.extends = extends
        self.fields = {}
        self.methods = {}
        self.params = params or []
        self.constructor = constructor_body
        if implements is not None:
            if type(implements) == str:
                self.implements = [implements]
            else:
                self.implements = implements


        self.type = Type.get(full_name)

        self.provides.add(full_name)
        if extends is not None:
            self.requires.add(extends)

    def get_var(self, prefix='', postfix=''):
        """ Get a Var associated with this class, named with optional
            pre-and postfixes.
        """
        if prefix is '' and postfix is '':
            if not hasattr(self, 'var_obj'):
                self.var_obj = Var(self.var_name, self.type)
            return self.var_obj
        elif prefix is not '':
            return Var(prefix + self.caps_name + postfix, self.type)
        else:
            return Var(self.var_name + postfix, self.type)

    def add_field(self, field):
        """ Add a field to this class. """
        self.fields[field.name] = field

    def remove_field(self, field):
        """ Remvoe a field from this class. """
        del self.fields[field.name]

    def add_method(self, method):
        """ Add a method to this class. """
        self.methods[method.name] = method

    def remove_method(self, method):
        """ Remove a method from this class. """
        del self.methods[method.name]

    def calculate_requires(self):
        """ Calculate requires needed to run the constructor. WARNING: This code's
            output should be manually verified.
        """
        if self.constructor is None:
            return set()
        requires = utils.parse_requires(self.constructor)
        for field in self.fields.values():
            if field.value is not None:
                requires.update(parse_requires(field.value))
        provided_statics = set(self.name + '.' + f.name for f in self.fields.values() if f.static)
        return requires - provided_statics - set(i.name for i in self.params)

    def compile(self, owner, compile_types=settings.compile_types):
        """ Perform actions to ready whatever this is for rendering """
        if compile_types:
            self.type.compile(self)
        for field_name, field in self.fields.iteritems():
            field.compile(self, compile_types=compile_types)
            self.provides.update(field.provides)
            self.requires.update(field.requires)
        for method_name, method in self.methods.iteritems():
            method.compile(self, compile_types=compile_types)
            self.provides.update(method.provides)
            self.requires.update(method.requires)

    def render_call(self, owner=None, default_args=None):
        """ Render what a call to the constructor would look like """
        return classrenderer.render_call(self, owner, default_args)

    def render(self, owner):
        """ Return a string containing what this would look like in code. """
        return classrenderer.render(self, owner)
