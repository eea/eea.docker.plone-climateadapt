
==============
Volto Subsites
==============

This add-on enable a new **Subsite** content-type and provides some utilities for Volto.


Subsite
-------

It's a basic folderish content with some additional fields:

- Header text
- Footer text
- Color
- Image

These fields are useful for Volto theme that will draw some components based on these values.

Accessing Subsite data from restapi
------------------------------------

There is a new expansion slot in restapi response when getting content data: `subsite`.

This expansion works like the standard ones (workflow, breadcrumbs, etc) and returns some metadata of the
parent Subsite if the requested content is inside a Subsite.

Control panel
-------------

There is a control panel that allows to set some settings for Subsites:

- Styles: you can set a predefined list of css classes that will be used in Volto theme to set some custom styles inside the subsite.


Translations
------------

This product has been translated into

- Italian


Installation
------------

Install collective.volto.subsites by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.volto.subsites


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.volto.subsites/issues
- Source Code: https://github.com/collective/collective.volto.subsites


License
-------

The project is licensed under the GPLv2.

Authors
=======

This product was developed by **RedTurtle Technology** team.

.. image:: https://avatars1.githubusercontent.com/u/1087171?s=100&v=4
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
