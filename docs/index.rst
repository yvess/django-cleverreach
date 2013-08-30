.. django-cleverreach documentation master file, created by
   sphinx-quickstart on Fri Aug 30 17:42:33 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django API for cleverreach
==========================

Contents:

.. toctree::
   :maxdepth: 2

   cleverreach.api


Installation
------------

``pip install django-cleverreach``

Add this to your ``settings.py`` ::

  CLEVERREACH = {'api_key': '<API KEY>',
                 'raise_exceptions': DEBUG,
  }


It's highly recommended to also put cleverreach list and form ids as well as the
user parameters in there, so you have them if you need them.
The easiest way to find the group id is by checking the URL of the group on
the receiver groups page.

Django-cleverreach uses the ``suds`` module: https://fedorahosted.org/suds/


Usage
-----
::

  import cleverreach.api
  client = cleverreach.api.Client()  # This opens up a connection to cleverreach.

you can silence errors by setting ``raise_exceptions`` to False.
In this case the module logs errors using the logger ``cleverreach.api``.

The module throws Exceptions of type ``cleverreach.CleverreachAPIException``
and ``suds.WebFault`` in case of a network error.


The currently supported API version is 5.1.


WARNING: cleverreach updates its APIs and turns old ones off without notice.
 Keep track of your installations and update this repository as needed.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

