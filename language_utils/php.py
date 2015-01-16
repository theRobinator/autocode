"""
Closure utilities.
"""

PRIMITIVE_TYPES = ['boolean', 'int', 'float', 'string', 'array', 'object', 'resource']
BUILT_IN_VARS = {'Infinity', 'NaN', 'null', 'undefined', 'true', 'false', 'window', 'document', 'this',  # Values
                 'alert', 'confirm', 'decodeURI', 'decodeURIComponent', 'encodeURI', 'encodeURIComponent', 'escape', 'eval', 'isFinite', 'isNaN', 'parseFloat', 'parseInt', 'clearTimeout', 'setTimeout', 'unescape',  # Functions
                 'Array', 'Boolean', 'Date', 'Function', 'Iterator', 'JSON', 'Math', 'Number', 'Object', 'String', 'Proxy', 'ParallelArray', 'RegExp',  # Base classes
                 'Error', 'EvalError', 'RangeError', 'ReferenceError', 'SyntaxError', 'TypeError', 'URIError'}  # Errors

PRIMITIVE_MAPPING = {
    'str': 'string',
    'string': 'string',
    'bool': 'boolean',
    'boolean': 'boolean',
    'int': 'int',
    'float': 'float',
    'long': 'float',
    'double': 'float'
}

PYTHON_CONTAINER_MAPPING = {
    'set': 'array',
    'list': 'array',
    'dict': 'object'
}

#: The doctags that appear in method or field signatures, so that they are redundant in comments.
REDUNDANT_DOCTAGS = {
    'param',
    'access',
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
