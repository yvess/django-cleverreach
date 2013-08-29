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
from cleverreach import CleverreachAPIException

from django.conf import settings
from django.test import TestCase
from ..api import Client

class User(object):  # Bunch class
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k not in self.__dict__:
                self.__dict__[k] = v



class TestTest(TestCase):

    def setUp(self):
        self.list1 = settings.CLEVERREACH['list1']
        self.list2 = settings.CLEVERREACH['list2']
        self.form1 = settings.CLEVERREACH['form1']
        self.form2 = settings.CLEVERREACH['form2']
        self.form3 = settings.CLEVERREACH['form3']
        self.client = Client()
        self.email1 = 'dc-test@spambog.com'
        self.email2 = 'dc-test2@spambog.com'

    def test_group_get_list(self):
        groups = self.client.group_get_list()
        group_names = [unicode(g.name) for g in groups]
        self.assertTrue('test1' in group_names)
        self.assertTrue('test2' in group_names)

    def test_forms_get_list(self):
        forms = self.client.forms_get_list(self.list1)
        self.assertEqual(len(forms), 1)
        obj = forms[0]
        self.assertTrue(isinstance(obj, object))
        self.assertEqual(obj.name, 'testform')
        self.assertEqual(obj.id, self.form1)

        forms = self.client.forms_get_list(self.list2)
        self.assertEqual(len(forms), 2)
        form_names = [f.name for f in forms]
        form_ids = [f.id for f in forms]
        self.assertTrue('testform2' in form_names)
        self.assertTrue('testform3' in form_names)
        self.assertTrue(self.form2 in form_ids)
        self.assertTrue(self.form3 in form_ids)

    def test_forms_get_code(self):
        code = self.client.forms_get_code(self.form1)
        self.assertTrue(isinstance(code, basestring))
        self.assertTrue('<form' in code)

    def test_forms_activation_mail(self):
        user1 = User(email=self.email1)
        user2 = User(email=self.email2)
        try:
            self.client.insert_new_user(user1, list_id=self.list2, activated=False,
                                        sendmail=False, form_id=self.form2)
            # create an already activated user
            self.client.insert_new_user(user2, list_id=self.list2, activated=True,
                                        sendmail=False, form_id=self.form2)

            response = self.client.forms_activation_mail(form_id=self.form2,
                                                         email=self.email1)
            self.assertEqual(response, self.email1)

            self.assertRaisesMessage(CleverreachAPIException,
                                        'subscriber allready active',
                self.client.forms_activation_mail, form_id=self.form2,
                                                  email=self.email2)


        finally:
            self.client.group_clear(self.list2)










