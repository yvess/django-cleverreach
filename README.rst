Django API for cleverreach
--------------------------

http://www.cleverreach.com/


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

The currently supported API version is 5.1.


Documentation
-------------

The documentation is on readthedocs.org:

http://django-cleverreach.readthedocs.org/en/latest/


WARNING: cleverreach updates its APIs and turns old ones off without notice.
 Keep track of your installations and update this repository as needed.


