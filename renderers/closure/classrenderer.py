from autocode.renderers.closure import typerenderer
from autocode import utils


def render(cls, owner):
    if cls.has_prop('extends'):
        cls.remove_all_props('extends')
    if cls.extends is not None:
        cls.add_prop('extends', cls.extends)

    if not cls.has_prop('constructor') and not cls.has_prop('interface'):
        cls.add_prop('constructor')

    cls.remove_all_props('param')
    for param in cls.params:
        if param.description:
            cls.add_prop('param', param.type, param.name + ' ' + param.description)
        else:
            cls.add_prop('param', param.type, param.name)

    result = ['/**', cls.render_comment(), ' */']

    result.append('%s = function(%s) {' % (cls.name, ', '.join(x.name for x in cls.params)))

    if cls.extends is not None and (cls.constructor is None or not cls.constructor.startswith('goog.base')):
        # If no goog.base is defined, add one
        result.append('    goog.base(this);')
    if cls.constructor is not None:
        # Indent the constructor body
        result.append('    ' + cls.constructor.replace("\n", "\n    "))
    result.append('};');
    if cls.extends is not None:
        result.append('goog.inherits(%s, %s);' % (cls.name, cls.extends))

    result.append("\n")

    # Fields
    if len(cls.fields) > 0:
        result.append("\n\n".join(x.render(cls) for x in utils.sort_fields(cls.fields.values())))
        result.append("\n")

    # Methods
    if len(cls.methods) > 0:
        result.append("\n\n".join(x.render(cls) for x in utils.sort_methods(cls.methods.values())))

    return "\n".join(result).replace('%C', cls.name)


def render_call(cls, owner=None, default_args=None):
    return typerenderer.render_call(cls.type, owner, default_args)
