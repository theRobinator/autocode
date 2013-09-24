from autocode.primitives.nameable import Nameable
from autocode.primitives.property import Property
from autocode.renderers import propertyrenderer
from autocode import utils


class Definable(Nameable):
    """ A piece of code that is definable. This includes everything that has properties.
    """

    #: The properties of this definable. This is a list of Property objects.
    #: Note that the number of items in the value tuples may vary.
    props = None

    #: The objects that this definable provides to the require graph.
    provides = None

    #: The objects that this definable requires from the require graph.
    requires = None

    #: The description of the definable, placed in its doc comment.
    description = None

    #: The visibility of the definable, usually something like 'public' or 'private'
    visibility = None

    def __init__(self, name, props=None, description='', visibility='public'):
        super(Definable, self).__init__(name)

        if props is None:
            self.props = []
        else:
            self.props = props

        self.provides = set([])
        self.requires = set([])
        self.description = description
        self.visibility = visibility

    def has_prop(self, prop_name):
        """ Check if this definable has a given property """
        return len(self.get_props(prop_name)) > 0

    def get_props(self, prop_name):
        """ Get a property by name """
        return [i for i in self.props if i.name == prop_name]

    def add_prop(self, name_or_property, modifier='', ident='', description=''):
        """ Add a single property.
            :param name_or_property: Either the string name of your property or a property object.
                                     If an object is specified, later parameters are ignored.
            :param modifier: The string modifier of a new property to add.
            :param ident: The string ident of a new property to add.
            :param description: The string description of a new property to add.
        """
        if isinstance(name_or_property, Property):
            self.props.append(name_or_property)
        else:
            self.props.append(Property(name_or_property, modifier, ident, description))

    def add_props(self, *props):
        """ Add multiple properties. This method only accepts Property objects. """
        self.props.extend(props)

    def remove_prop(self, name_or_property, modifier='', ident='', description=''):
        """ Remove a single property.
            :param name_or_property: Either the string name of a property or a property object.
                                     If an object is specified, later parameters are ignored.
            :param modifier: The string name of a property's modifier.
            :param ident: The string identifier of a property.
            :param description: The string description of a property.
        """
        if isinstance(name_or_property, Property):
            self.props.remove(name_or_property)
        else:
            self.props.remove(Property(name_or_property, modifier, ident, description))

    def remove_all_props(self, name, modifier=None, ident=None, description=None):
        """ Remove all properties matching a set of values. If incomplete values are passed, all
            values matching are removed. For example, calling this with 'param' will remove all
            param tags from a definition.
        """
        def test(p):
            return p.name == name and \
                   (modifier is None or p.modifier == modifier) and \
                   (ident is None or p.ident == ident) and \
                   (description is None or p.description == description)

        self.props = [prop for prop in self.props if not test(prop)]

    def clear_props(self):
        """ Remove all props from this definable. """
        self.props = []

    def render_comment(self):
        """ Render all properties of this definable into comment form.
            :return: string
        """
        return propertyrenderer.render_comment(self.props, self.description)
