from autocode.renderers import annotationrenderer


class Annotation(object):
    """ A variable, with a name and a type.
    """

    #: The annotation's name
    name = None

    #: Arguments of the annotation
    args = None

    def __init__(self, name, arg=None):
        self.name = name
        if arg is not None:
            if type(arg) == str:
                self.args = [arg]
            else:
                self.args = arg
        else:
            self.args = []


    def compile(self, owner, parent_class=None):
        """ Perform actions to ready whatever owns this for rendering """
        pass

    def render(self, owner=None):
        """ Return a string containing what this would look like in code. """
        return annotationrenderer.render(self, owner)