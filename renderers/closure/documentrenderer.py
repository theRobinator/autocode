def render(doc, sort_fields=True):
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

    if sort_fields:
        strings = []
        fields = []
        enums = []
        functions = []
        classes = []
        sort_map = [(str, strings), (Field, fields), (Enum, enums), (Function, functions), (Class, classes)]
        for item in doc.items:
            for field_type, render_array in sort_map:
                if isinstance(item, field_type):
                    # enum is an instance of Class, skip render to avoid rendering enum twice
                    if type(item) is Enum and field_type is Class:
                        continue
                    elif type(item) == str:
                        text = item
                    else:
                        text = item.render(doc)
                    if len(text) > 0:
                        render_array.extend(["\n\n", text])

        result.extend(strings)
        result.extend(functions)
        result.extend(classes)
        result.extend(fields)
        result.extend(enums)
    else:
        for item in doc.items:
            if type(item) == str:
                text = item
            else:
                text = item.render(doc)
            if len(text) > 0:
                result.extend(["\n", text])

    return "\n".join(result)
