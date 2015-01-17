"""
Closure utilities.
"""

PRIMITIVE_TYPES = ['string', 'number', 'boolean', 'Array', 'Object', 'Function']
BUILT_IN_VARS = {'Infinity', 'NaN', 'null', 'undefined', 'true', 'false', 'window', 'document', 'this',  # Values
                 'alert', 'confirm', 'decodeURI', 'decodeURIComponent', 'encodeURI', 'encodeURIComponent', 'escape', 'eval', 'isFinite', 'isNaN', 'parseFloat', 'parseInt', 'clearTimeout', 'setTimeout', 'unescape',  # Functions
                 'Array', 'Boolean', 'Date', 'Function', 'Iterator', 'JSON', 'Math', 'Number', 'Object', 'String', 'Proxy', 'ParallelArray', 'RegExp',  # Base classes
                 'Error', 'EvalError', 'RangeError', 'ReferenceError', 'SyntaxError', 'TypeError', 'URIError'}  # Errors

PRIMITIVE_MAPPING = {
    'str': 'string',
    'string': 'string',
    'bool': 'boolean',
    'boolean': 'boolean',
    'int': 'number',
    'float': 'number',
    'long': 'number',
    'double': 'number'
}

PYTHON_CONTAINER_MAPPING = {
    'set': 'Array',
    'list': 'Array',
    'dict': 'Object'
}

#: The doctags that appear in method or field signatures, so that they are redundant in comments.
REDUNDANT_DOCTAGS = {

}

EMPTY_COMMENT = ' *'

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
        return (not item.static, item.type is None, item.has_prop('private'), not item.has_prop('inheritDoc'),
                item.name)
    return sorted(fields, key=sortKey)


def sort_methods(funcs):
    """ Sort functions into an ordered list. """
    def sortKey(item):
        return (not item.static, item.has_prop('private'), not item.has_prop('inheritDoc'), not item.has_prop('override'),
                item.name)
    return sorted(funcs, key=sortKey)


def parse_requires(code):
    """ Parse out required symbols from raw code. This will include everything
        that is not defined in the code itself, except for built-in symbols.
    """

    def _parse_dots(node):
        parts = []
        while node.type == 'DOT':
            parts.insert(0, node.value)
            node = node[0]
        if node.type == 'IDENTIFIER':
            parts.insert(0, node.value)
            return '.'.join(parts)
        else:
            return None

    def _analyze_statement(tree, usages=None):
        if usages is None:
            usages = set()

        declared_props = set()
        try:
            node_type = tree.type
        except:
            import ipdb; ipdb.set_trace()
        parse_index = 0


        if node_type == 'RETURN' and tree.value != 'return':
            _analyze_statement(tree.value, usages)
        elif node_type == 'NEW' or node_type == 'NEW_WITH_ARGS':
            name = _parse_dots(tree[0])
            if name is not None:
                usages.add(name)
                parse_index = 1
        elif node_type == 'DOT':
            name = _parse_dots(tree[0])
            if name is not None:
                usages.add(name)
                parse_index = 1
            else:
                _analyze_statement(tree[0], usages)
            parse_index = 2
        elif node_type == 'PROPERTY_INIT':
            # Special case because this doesn't count as a usage
            parse_index = 1
        elif node_type == 'INSTANCEOF':
            # instanceof calls get special treatment because they use class names
            _analyze_statement(tree[0], usages)
            name = _parse_dots(tree[1])
            if name is not None:
                usages.add(name)
                parse_index = 2
            else:
                parse_index = 1
        elif node_type == 'IDENTIFIER':
            usages.add(_parse_dots(tree))
        elif node_type == 'FUNCTION':
            declared_props.update(tree.params)
        elif node_type == 'IF':
            _analyze_statement(tree.condition, usages)
            if tree.thenPart:
                _analyze_statement(tree.thenPart, usages)
            if tree.elsePart:
                _analyze_statement(tree.elsePart, usages)
        elif node_type == 'SWITCH':
            for case in tree.cases:
                _analyze_statement(case, usages)
        elif node_type == 'CASE':
            _analyze_statement(tree.caseLabel, usages)
            for stmt in tree.statements:
                _analyze_statement(stmt, usages)

        # Now jump into the right sub-trees
        if hasattr(tree, 'expression') and tree.expression is not None:
            _analyze_statement(tree.expression, usages)

        if hasattr(tree, 'initializer') and tree.initializer is not None:
            _analyze_statement(tree.initializer, usages)

        if hasattr(tree, 'body') and tree.body is not None:
            _analyze_statement(tree.body, usages)


        # No need to parse symbols we've already gone over
        for i in xrange(parse_index, len(tree)):
            _analyze_statement(tree[i], usages)

        usages -= declared_props

        return usages

    # Use a library to create an AST
    try:
        tree = jsparser.parse('function dummy() { ' + code + "\n}")  # Dummy function wrapper prevents syntax errors for returns outside functions
    except jsparser.SyntaxError_, err:
        print 'JS syntax error: %s' % err
        print 'Code was:'
        print code
        return set()
    requires = set()

    script = tree[0].body
    #import ipdb; ipdb.set_trace()
    # Get all the symbols that are used
    for statement in script:
        requires.update(_analyze_statement(statement))

    # Remove all the variables that were defined
    defined = set()
    for var in script.varDecls:
        defined.add(var.value)
    requires -= defined

    # Remove the built-ins and superglobals
    requires -= BUILT_IN_VARS
    requires -= set(['goog', 'zoosk', 'soy'])

    return requires
