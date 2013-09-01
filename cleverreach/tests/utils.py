# coding: utf-8

import datetime, time
from django.conf import settings
from django.test import TestCase
from ..api import Client
from ..utils import User, insert_new_user

class TestUtils(TestCase):

    def setUp(self):
        self.list1 = settings.CLEVERREACH['list1']
        self.list2 = settings.CLEVERREACH['list2']
        self.form1 = settings.CLEVERREACH['form1']
        self.form2 = settings.CLEVERREACH['form2']  # email only
        self.form3 = settings.CLEVERREACH['form3']
        self.client = Client()
        self.email1 = 'dc-test@spambog.com'
        self.email2 = 'dc-test2@spambog.com'

    def test_insert_new_user(self):
        try:
            user1 = User(email=self.email1)
            user2 = {'email': self.email2 }
            client = self.client

            data = insert_new_user(user1, self.list1, activated=True,
                                   sendmail=False, form_id=self.form1)
            self.assertEqual(data.email, self.email1)
            self.assertEqual(data.active, True)
            self.assertEqual(data.source, 'API')

            data = insert_new_user(user2, self.list1, activated=False,
                                   sendmail=False, form_id=self.form1)
            self.assertEqual(data.email, self.email2)
            self.assertEqual(data.active, False)
            self.assertEqual(data.source, 'API')
        finally:
            self.client.group_clear(self.list1)