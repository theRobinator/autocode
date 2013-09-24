def render(doc):
    """ Return a string containing what a document would look like in code. """
    result = []

    if len(doc.provides) > 0:
        result.append("\n".join(("goog.provide('%s');" % provide) for provide in sorted(doc.provides)))
        if len(doc.requires) > 0:
            result.append('')

    if len(doc.requires) > 0:
        result.append("\n".join(("goog.require('%s');" % require) for require in sorted(doc.requires)))

    # Sort the items by type
    from autocode.primitives.cls import Class
    from autocode.primitives.enum import Enum
    from autocode.primitives.field import Field
    from autocode.primitives.function import Function

    fields = []
    enums = []
    functions = []
    classes = []
    sort_map = [(Field, fields), (Enum, enums), (Function, functions), (Class, classes)]

    for item in doc.items:
        for field_type, render_array in sort_map:
            if isinstance(item, field_type):
                text = item.render(doc)
                if len(text) > 0:
                    render_array.extend(["\n\n", text])

    result.extend(functions)
    result.extend(classes)
    result.extend(fields)
    result.extend(enums)

    return "\n".join(result)
