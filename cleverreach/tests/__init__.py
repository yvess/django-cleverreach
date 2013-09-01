# coding: utf-8
""" Test configuration in cleverreach:

    group test_1 with one form with the following fields:
    testform: first_name, last_name, salutation, email

    group test_2 with two forms with the following fields:
    testform2: email
    testform3: testemail, comments (Textarea), amount (number),
               when (date TT.MM.JJJJ, required)

    create a file called secrets.py and add the following settings:

    CLEVERREACH = {'api_key': '???',
                'list1': ???,
                'list2': ???,
                'form1': ???,
                'form2': ???,
                'form3': ???,
              }

"""

from .api_v51 import *
from .utils import *