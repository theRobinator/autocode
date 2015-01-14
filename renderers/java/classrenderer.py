from autocode.renderers.java import typerenderer
from autocode import utils


def render(cls, owner):
    cls.remove_all_props('param')
    constructor_params = cls.params
    cls.params = []

    result = ['/**', ' */']

    inheritance_string = ''
    if cls.extends is not None:
        inheritance_string += ' extends %s' % cls.extends
    if cls.implements is not None:
        inheritance_string += ' implements %s' % ', '.join(cls.implements)
    result.append("class %s%s {" % (cls.name, inheritance_string))
    indent_result = []

    if cls.enums is not None:
        indent_result.append("\n")
        indent_result.extend(x.render(cls) for x in (cls.enums.values()))
        indent_result.append("\n")

    # Fields
    if len(cls.fields) > 0:
        indent_result.extend(x.render(cls) for x in utils.sort_fields(cls.fields.values()))
        indent_result.append("\n")

    from autocode.primitives import Function

    if cls.constructor is not None and cls.constructor != '':
        constructor_func = Function(cls.name, params=constructor_params)
        constructor_func.visibility = cls.visibility
        constructor_func.body = cls.constructor
        constructor_func.compile(cls)
        indent_result.append(constructor_func.render(cls))

    indent_result.append('')

    # Methods
    if len(cls.methods) > 0:
        methods = []
        preferred_methods = set()
        for preferred_method in cls._method_order:
            methods.append(cls.methods[preferred_method])
            preferred_methods.add(preferred_method)
        methods.extend(v for v in utils.sort_methods(cls.methods.values()) if v.name not in preferred_methods)

        indent_result.append("\n\n".join(x.render(cls) for x in methods))

    # Indent the class body
    result.append('    ' + "\n".join(indent_result).replace("\n", "\n    "))
    result.append("\n}")

    return "\n".join(result).replace('%C', cls.name)


def render_call(cls, owner=None, default_args=None):
    return typerenderer.render_call(cls.type, owner, default_args)
