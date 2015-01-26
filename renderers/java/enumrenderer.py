from autocode import utils
from autocode import settings

def render(enum, owner):
    enum.remove_all_props('param')
    constructor_params = enum.params
    if enum.value_type is None:
        raise Exception('Enums must have type')

    if enum.extends is not None:
        raise Exception('Enums cannot extend other classes')

    comments = enum.render_comment()
    if comments == utils.EMPTY_COMMENT and settings.get_redundant_doctag_setting() is False:
        result = []
    else:
        result = ['/**', comments, ' */']

    indent_result = []
    implements_string = ''
    if enum.implements is not None:
        implements_string += ' implements %s' % ', '.join(enum.implements)


    indent_result.append("%s enum %s%s {" % (enum.visibility, enum.name, implements_string))
    i = 1
    for key, value in sorted(enum.values):
        if value is None:
            enum_str = key
        else:
            enum_str = "%s(%s)" % (key, value)

        if i < len(enum.values):
            indent_result.append(enum_str + ',')
        else:
            indent_result.append(enum_str + ';')
        i += 1

    # Fields
    if len(enum.fields) > 0:
        indent_result.append("\n")
        indent_result.extend(x.render(enum) for x in utils.sort_fields(enum.fields.values()))
        indent_result.append("\n")

    from autocode.primitives import Function
    if enum.constructor is not None and enum.constructor != '':
        constructor_func = Function(enum.name, params=constructor_params)
        constructor_func.visibility = enum.visibility
        constructor_func.body = enum.constructor
        constructor_func.compile(enum)
        indent_result.append(constructor_func.render(enum))
        indent_result.append('')



    if len(enum.methods) > 0:
        methods = []
        preferred_methods = set()
        for preferred_method in enum._method_order:
            methods.append(enum.methods[preferred_method])
            preferred_methods.add(preferred_method)
        methods.extend(v for v in utils.sort_methods(enum.methods.values()) if v.name not in preferred_methods)

        indent_result.append("\n\n".join(x.render(enum) for x in methods))

    result.append("\n".join(indent_result).replace("\n", "\n    "))
    result.append('}')
    return "    \n".join(result)
