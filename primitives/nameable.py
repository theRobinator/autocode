from autocode.renderers import namerenderer


class Nameable(object):
    """ A nameable is anything in code that can be named. """

    #: The original name of the object. In languages where classes are namespaced, this is the only name with the full spacing.
    name = ''

    #: A version of the name usable in private fields.
    private_name = ''

    #: A version of the name useable in public fields.
    public_name = ''

    #: A version of the name usable in class names.
    class_name = ''

    #: A version of the name usable in variable names.
    var_name = ''

    def __init__(self, name):
        self.name = name
        normal_name = namerenderer.normalize_name(name)
        self.private_name = namerenderer.privatize_name(normal_name)
        self.public_name = namerenderer.publicize_name(normal_name)
        self.class_name = namerenderer.classify_name(normal_name)
        self.var_name = namerenderer.varify_name(normal_name)

    def __str__(self):
        return self.name
