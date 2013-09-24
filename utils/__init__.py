"""
The magic file!

This file acts as a front end for the files in the utils directory. Since only one util module is
ever supposed to be used (the one for the current language), importing this module will cause it to
determine the correct module based on the language, then seamlessly add all of its declared methods
to itself. That means that when the language is set to 'closure', these are equivalent:
from autocode.utils import closure as utils
from autocode import utils
"""

from autocode import settings

# Import the correct module based on the language in settings
currentlang = __import__('autocode.utils.%s' % settings.language, globals(), locals(), ['autocode.utils'])

# Run through the non-private attributes declared on the module and declare them on this one
attrs = [i for i in dir(currentlang) if not i.startswith('_')]
for i in attrs:
    locals()[i] = getattr(currentlang, i)

# Don't pollute the module with local variables
del i
del attrs
