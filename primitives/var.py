from autocode.primitives.nameable import Nameable
from autocode.primitives.autocode_type import Type


class Var(Nameable):
    """ A variable, with a name and a type.
    """

    #: The variable's type.
    type = None

    #: An optional value.
    value = None

    def __init__(self, name, var_type, value=None):
        if type(var_type) == str:
            var_type = Type.get(var_type)
        super(Var, self).__init__(name)
        self.type = var_type
        self.value = value
