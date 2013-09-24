from autocode.primitives.nameable import Nameable
from autocode.primitives.type import Type


class Var(Nameable):
    """ A variable, with a name and a type. This does not support value assignment
        specificaly because you should not be writing that in a templating language.
    """

    #: The variable's type.
    type = None

    def __init__(self, name, var_type):
        if type(var_type) == str:
            var_type = Type.get(var_type)
        super(Var, self).__init__(name)
        self.type = var_type
