.. _readme:

########
Autocode
########

.. toctree::
   :maxdepth: 1

Autocode is a programming efficiency library. Have you ever found yourself
writing repetetive code? Do you hate creating interfaces or adding setters and
getters one-by-one to your new model classes? Then Autocode is for you!

The Autocode library lets you write succinct Python code instead of whatever
language you've decided to use. It then generates your language based on its
specifications.

.. note::

  This library is a templating system to replace copy/paste only. If you find
  yourself writing code specific to one or two files in it, you're doing it wrong.
  As a rule of thumb, if you have to write something twice or more it should show
  up in Python; otherwise it should be written in your actual code.

.. warning::

  Autocode is currently in (heavy) developemnt. It currently supports only
  JavaScript using the Google Closure framework for documentation. Feel free to
  fork this library and add your own renderers, however!


Installation
============

Autocode is currently in development, so installing it means adding the directory
*containing* the autocode folder to your ``$PYTHONPATH``. That means running
something like::

  export PYTHONPATH="/path/to/folder:$PYTHONPATH"

Choosing a Language
-------------------

The next thing you will want to do is choose a language. Modify the settings.py
file in the root of the checkout so that the ``language`` variable is set to
the language that you want to use. You may also want to modify other settings
before you run the code.


Writing an Autocode Program
===========================

Once you've installed the library, you can start making use of it. There are
seven different classes available to you, all available in the ``autocode.primitives``
package:

* **Type**: A type, that exists for a variable, field, or class.
* **Var**: A variable, with a name and a type. These mostly appear in parameter lists.
* **Field**: A field that exists in a class or a document.
* **Enum**: An enum.
* **Function**: A function that exists in a class or document.
* **Class**: A class.
* **Document**: A document that contains the other primitive types.

A Simple Class
--------------

For the purposes of examples, we'll be generating JavaScript. Let's say we do this code::

    from autocode.primitives import *
    
    document = Document()
    cls = Class('Example', extends='AbstractView')
    document.add_items(cls)
    print document.render()

This will output the following Javascript document:

.. code-block:: js

    goog.provide('Example');
    goog.require('AbstractView');

    /**
     * @extends {AbstractView}
     * @constructor
     */
    Example = function() {
        goog.base(this);
    };
    goog.inherits(Example, AbstractView);

This is the general structure of how a program using Autocode should work. Items are
instantiated and added to a document, and then the document is rendered. You can use
different options in constructors and modify the added items to change what the output of
``document.render()`` is.


A More Complex Class
--------------------

Let's add some fields and methods to this class::

    from autocode.primitives import *
    document = Document()

    cls = Class('Example', extends='AbstractView')

    cls.add_field(Field('myField', 'Object', static=True))
    cls.add_field(Field('privateField_', 'string', visibility='private'))

    cls.add_method(Function('dance', return_type='boolean', body='return true;'))

    document.add_items(cls)
    print document.render()

This code outputs a much longer file:

.. code-block:: js

    goog.provide('Example');
    goog.require('AbstractView');

    /**
     * @extends {AbstractView}
     * @constructor
     */
    Example = function() {
        goog.base(this);
    };
    goog.inherits(Example, AbstractView);

    /**
     * @type {Object}
     */
    Example.myField;

    /**
     * @private
     * @type {string}
     */
    Example.prototype.privateField_;

    /**
     * @return {boolean}
     */
    Example.prototype.dance = function() {
        return true;
    };

We can see that the information expressed is the same in both the Autocode and the
actual JS, except that the JS code is much larger. It's also important to note
that we didn't do anything that had to do with JavaScript in our source code.
If you wanted to generate PHP code, you'd only have to change the setting in
your settings file and re-run the program.


Adding New Languages
====================

Autocode is currently in development, so you may not see the language that you
want available. If you're ready to help solve that problem, you can add your
own languages (and contributing them would be appreciated). Let's take a short
trip into how Autocode produces the code you know and love:

1. The settings.py file lists a string as the target language.
2. The renderers module checks for a sub-module of that name.
3. The utils module checks for a sub-module of that name.

So, in order to implement new languages, you'll need to create new sub-modules.
Just copy and paste every file in the modules, then modify them to your own
liking so that they return language-specific things.
