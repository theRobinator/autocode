from autocode.renderers import annotationrenderer


class Annotation(object):
    """ An Annotation has a name and optional arguments
    """

    #: The annotation's name
    name = None

    #: Arguments of the annotation
    args = None

    def __init__(self, name, args=None):
        """
        :param name: the annotation's name
        :param args: the arguments that apply to the annotation

        Example usage 1: Annotation('Override', "'unchecked'") produces @Override('unchecked') in java
        Example usage 2: Annotation('Schedule', ['dayofWeek=\"Fri\"', 'hour=\"23\"']produces  @Schedule(dayOfWeek="Fri", hour="23") in java
        """
        self.name = name
        if args is not None:
            if type(args) == str:
                self.args = [args]
            else:
                self.args = args
        else:
            self.args = []


    def compile(self, owner, parent_class=None):
        """ Perform actions to ready whatever owns this for rendering """
        pass

    def render(self, owner=None):
        """ Return a string containing what this would look like in code. """
        return annotationrenderer.render(self, owner)