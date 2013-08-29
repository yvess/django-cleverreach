Django API for cleverreach
--------------------------

http://www.cleverreach.com/


Installation
------------

1.  ``pip install django-cleverreach``

2. Add this to your ``settings.py``::

  CLEVERREACH = {'api_key': '<API KEY>',}


It's highly recommended to also put cleverreach list and form ids as well as the
user parameters in there, so you have them if you need them.

Django-cleverreach uses the ``suds`` module: https://fedorahosted.org/suds/


Usage
-----
::

  import cleverreach.api
  client = cleverreach.api.Client()  # This opens up a connection to cleverreach.

you can silence errors by using::

  client = cleverreach.api.Client(raise_exceptions=False)



WARNING: cleverreach updates its APIs and turns old ones off without notice.
 Keep track of your installations and update this repository as needed.


