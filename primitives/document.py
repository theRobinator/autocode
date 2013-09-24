from autocode.renderers import documentrenderer
from autocode import settings


class Document(object):
    """ A document, containing zero or more definables. Its primary function is
        to manage provides and requires. It is also the main interface to the
        programmer that will have compile() called on it.
    """

    #: The name of the document; this is sometimes used as a top-level static prefix
    name = ''

    #: All identifiers that are provided by this document.
    provides = None

    #: All identifiers required by this document.
    requires = None

    #: All items in this document.
    items = None

    #: Whether this document has been compiled.
    _compiled = False

    def __init__(self, static_name=None):
        self.items = []
        self.name = static_name
        self.provides = set()
        self.requires = set()

    def add_items(self, *items):
        """ Add one or more items to this document. """
        self.items.extend(items)

    def get_item(self, name):
        """ Get an item by name. """
        for i in self.items:
            if i.name == name:
                return i
        return None
    
    def compile(self, compile_types=settings.compile_types):
        """ Perform actions to ready the document for rendering. """
        for item in self.items:
            item.compile(self, compile_types=compile_types)
        for item in self.items:
            if hasattr(item, 'provides'):
                self.provides.update(item.provides)
            if hasattr(item, 'requires'):
                self.requires.update(item.requires)
        self.requires -= self.provides
        self._compiled = True

    def render(self):
        """ Return a string containing what this would look like in code. """
        if not self._compiled:
            self.compile()
        return documentrenderer.render(self)
