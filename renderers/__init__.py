"""
The magic file!

This file abstracts the user's choice of language by using a magic adapter class to forward attribute requests to other
modules. That means that although it's possible to do
from autocode.renderers.closure import classrenderer
but if you have set the language to closure, it's functionally equivalent to do
from autocode.renderers import classrenderer
However, if you do the second one, your code will automatically adapt to the correct language.
"""

from autocode import MagicAdapter


classrenderer = MagicAdapter('autocode.renderers', 'classrenderer')
documentrenderer = MagicAdapter('autocode.renderers', 'documentrenderer')
enumrenderer = MagicAdapter('autocode.renderers', 'enumrenderer')
fieldrenderer = MagicAdapter('autocode.renderers', 'fieldrenderer')
interfacerenderer = MagicAdapter('autocode.renderers', 'interfacerenderer')
functionrenderer = MagicAdapter('autocode.renderers', 'functionrenderer')
namerenderer = MagicAdapter('autocode.renderers', 'namerenderer')
propertyrenderer = MagicAdapter('autocode.renderers', 'propertyrenderer')
typerenderer = MagicAdapter('autocode.renderers', 'typerenderer')
valuerenderer = MagicAdapter('autocode.renderers', 'valuerenderer')
