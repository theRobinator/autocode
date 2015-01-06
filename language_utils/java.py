"""
Java utilities.
"""

PRIMITIVE_TYPES = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char', 'String']
"""
Java utilities.
"""

PRIMITIVE_TYPES = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char', 'String']
BUILT_IN_VARS = {'true', 'false', 'null', 'this',  # Values
                 'String', 'Object', 'Boolean', 'Integer', 'Double', 'Float', 'Char', 'Long', 'Array', 'Math', 'BigInteger', # Base classes
                 'ArithmeticException', 'ArrayIndexOutOfBoundsException', 'ArrayStoreException', 'ClassCastException', 'IllegalArgumentException', 'IllegalMonitorStateException', 'IllegalStateException', 'IllegalThreadStateException',
                 'IndexOutOfBoundsException', 'NegativeArraySizeException', 'NullPointerException', 'NumberFormatException', 'SecurityException', 'StringIndexOutOfBounds', 'UnsupportedOperationException'}  # Errors
PRIMITIVE_MAPPING = {
    'str': 'String',
    'string': 'String',
    'bool': 'boolean',
    'boolean': 'boolean',
    'int': 'int',
    'float': 'float',
    'long': 'long',
    'double': 'double'
}

PYTHON_CONTAINER_MAPPING = {
    'set': 'Set',
    'list': 'List',
    'dict': 'HashMap'
}


def is_primitive_type(ctype):
    if type(ctype) == str:
        return ctype in PRIMITIVE_TYPES
    else:
        return ctype.name in PRIMITIVE_TYPES


def is_private(name_or_nameable):
    """ Determine if a given name or Nameable instance is private.
        :param name_or_nameable: The thing to test.
        :type name_or_nameable: string|Nameable
    """
    if isinstance(name_or_nameable, str):
        name = name_or_nameable
    else:
        name = name_or_nameable.name

    return name.endswith('_')


def sort_fields(fields):
    """ Sort an iterable of fields into an ordered list. Sort order is static
        then instance, public then private, and inheritDoc, typed, and non-typed
    """
    def sortKey(item):
        return (not item.const, not item.static, item.type is None, item.has_prop('private'), item.name)
    return sorted(fields, key=sortKey)


def sort_methods(funcs):
    """ Sort functions into an ordered list. """
    def sortKey(item):
        return (not item.static, item.has_prop('private'), item.name)
    return sorted(funcs, key=sortKey)
