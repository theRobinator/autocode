"""
The magic file!

This file abstracts the user's choice of language by copying all of the language-specific declarations
onto the main renderers module. That means that although it's possible to do
from autocode.renderers.closure import classrenderer
if you have set the language to closure, it's functionally equivalent to do
from autocode.renderers import classrenderer
However, if you do the second one, your code will automatically adapt to the correct language.
"""

from autocode.settings import language


classrenderer = __import__('autocode.renderers.%s.classrenderer' % language, fromlist=['autocode.renderers', language])
documentrenderer = __import__('autocode.renderers.%s.documentrenderer' % language, fromlist=['autocode.renderers', language])
enumrenderer = __import__('autocode.renderers.%s.enumrenderer' % language, fromlist=['autocode.renderers', language])
fieldrenderer = __import__('autocode.renderers.%s.fieldrenderer' % language, fromlist=['autocode.renderers', language])
interfacerenderer = __import__('autocode.renderers.%s.interfacerenderer' % language, fromlist=['autocode.renderers', language])
functionrenderer = __import__('autocode.renderers.%s.functionrenderer' % language, fromlist=['autocode.renderers', language])
namerenderer = __import__('autocode.renderers.%s.namerenderer' % language, fromlist=['autocode.renderers', language])
propertyrenderer = __import__('autocode.renderers.%s.propertyrenderer' % language, fromlist=['autocode.renderers', language])
typerenderer = __import__('autocode.renderers.%s.typerenderer' % language, fromlist=['autocode.renderers', language])
