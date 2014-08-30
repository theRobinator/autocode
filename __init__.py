from autocode import language_utils


class MagicAdapter(object):
    """ Magic class that redirects each call to it to the contained renderer module.
    """
    #: The dict of language modules available.
    available_languages = None

    #: The current module full of renderers.
    current_module = None

    #: The parent of the module for importing.
    parent_module = None

    #: The submodule name of an instance of the MagicAdapter.
    submodule_name = None

    def __init__(self, parent_module, submodule_name=None):
        self.parent_module = parent_module
        self.submodule_name = submodule_name
        self.available_languages = {}

    def __getattr__(self, item):
        if item == 'submodule_name':
            return self.submodule_name

        from autocode.settings import get_language
        language_name = get_language()
        if language_name not in self.available_languages:
            if self.submodule_name is None:
                import_name = '%s.%s' % (self.parent_module, language_name)
            else:
                import_name = '%s.%s.%s' % (self.parent_module, language_name, self.submodule_name)
            mod = __import__(import_name, fromlist=[self.parent_module, language_name])
            self.available_languages[language_name] = mod
        else:
            mod = self.available_languages[language_name]

        return getattr(mod, item)

# The utils module is one of the modules in the utils folder
utils = MagicAdapter('autocode.language_utils')
