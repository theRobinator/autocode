from autocode.renderers.closure import typerenderer
from autocode import utils


def render(cls, owner):
    cls.remove_all_props('param')
    constructor_params = cls.params
    cls.params = []

    result = ['/**', ' */']

    inheritance_string = ''
    if cls.extends is not None:
        inheritance_string += ' extends %s' % cls.extends
    result.append('class %s%s {' % (cls.name, inheritance_string))
    indent_result = []

    # Fields
    if len(cls.fields) > 0:
        indent_result.extend(x.render(cls) + "\n" for x in utils.sort_fields(cls.fields.values()))
        indent_result.append("\n")

    # Constructor
    constructor_body = ''
    if cls.extends is not None and (cls.constructor is None or not cls.constructor.startswith('parent::__construct();')):
        # If no goog.base is defined, add one
        cls.constructor = 'parent::__construct();' + cls.constructor

    from autocode.primitives import Function
    constructor_func = Function('__construct', params=constructor_params)
    constructor_func.visibility = cls.visibility
    constructor_func.body = cls.constructor
    constructor_func.compile(cls)
    indent_result.append(constructor_func.render(cls))

    indent_result.append('')

    # Methods
    if len(cls.methods) > 0:
        indent_result.append("\n\n".join(x.render(cls) for x in utils.sort_methods(cls.methods.values())))

    # Indent the class body
    result.append('    ' + "\n".join(indent_result).replace("\n", "\n    "))
    result.append("\n}")

    return "\n".join(result).replace('%C', cls.name)


def render_call(cls, owner=None, default_args=None):
    return typerenderer.render_call(cls.type, owner, default_args)
