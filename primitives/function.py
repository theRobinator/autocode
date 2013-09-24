from autocode.primitives.definable import Definable
from autocode.primitives.document import Document
from autocode.primitives.type import Type
from autocode.renderers import functionrenderer
from autocode.renderers import namerenderer
from autocode import utils


class Function(Definable):
    """ A function! :D """

    #: This function's parameters as a list of Vars.
    params = None

    #: The return type.
    return_type = None

    #: The body of the function.
    body = None

    #: Whether the function is static.
    static = False

    def __init__(self, name, params=None, return_type=None, body='', static=False, visibility='public', props=None):
        super(Function, self).__init__(name, props=props, visibility=visibility)

        self.params = params or []
        if type(return_type) == str:
            return_type = Type.get(return_type)
        self.return_type = return_type
        self.body = body
        self.static = static

    def calculate_requires(self):
        """ Calculate requires needed to run this function. WARNING: This code's
            output should be manually verified.
        """
        if self.body is None:
            return set()
        requires = utils.parse_requires(self.body)
        return requires - set(i.name for i in self.params)

    def compile(self, owner, compile_types=True):
        """ Perform actions to ready whatever this is for rendering """
        if owner is None or isinstance(owner, Document):
            self.static = True

    def render_call(self, owner=None, default_args=None):
        """ Return what a call to this function would look like """
        return functionrenderer.render_call(self, owner, default_args)

    def render(self, owner):
        """ Return a string containing what this would look like in code. """
        return functionrenderer.render(self, owner)
