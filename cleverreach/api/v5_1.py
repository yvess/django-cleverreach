# coding: utf-8

"""
You have to define a group (in the cleverreach admin panel) for each language.
The form code is optional, we use the first form if it is not provided.

The Cleverreach API requires suds: https://fedorahosted.org/suds/

You have to define the following parameters in your settings.py:

    CLEVERREACH = {'api_key': '<API KEY>',
                    'groups': {'nl_de': '<GROUP-ID>',
                               'nl_fr': '<GROUP-ID>'},
                  }

Currently the groups parameter is not used but it forces you to write it down
because you will need it at some point.
"""

import datetime, time

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from suds.client import Client
from suds import WebFault


URL = 'http://api.cleverreach.com/soap/interface_v5.1.php?wsdl'
API_KEY = settings.CLEVERREACH.get('api_key')

ANREDE = {'male': _('Herr'), 'female': _('Frau')}

soap = None

class Client(object):

    def __init__(self):
        self.soap = Client(URL)  #immediately opens up a connection.


    """ Forms have the format [(name){id, name, description}] """
    def get_forms(self, group_id):
        try:
            query = self.soap.service.formsGetList(API_KEY, group_id)
        except WebFault, e:
            return e
        return query.data

    def send_activation_mail(self, form_id, email):
        """Will send the activation mail to the given email"""
        try:
            query = self.soap.service.formsActivationMail(API_KEY, form_id, email)
        except WebFault, e:
            return e
        return query.data

    def get_by_email(self, list_id, email):
        try:
            query = self.soap.service.receiverGetByEmail(API_KEY, list_id, email, 1)
        except WebFault, e:
            return e
        return query.data

    def get_form_code(self, form_id):
        try:
            query = self.soap.service.formsGetCode(API_KEY, form_id)
        except WebFault, e:
            return e
        return query.data


    def get_group_list(self):
        try:
            query = self.soap.service.groupGetList(API_KEY)
        except WebFault, e:
            return e
        return query.data

    def insert_new_user(self, user, group_id, activated=False, sendmail=True,
                        form_id=None, attrs=None):
        """ The default form only accepts email, registered, activated, source and attributes.
            To add more fields you have to add them as attributes. Make sure the keys
            are the same as the name of the fields in the form. (Check with get_by_email)

            `attrs` needs to be a list in the form ['first_name', 'last_name'] and
            the attribute must exist on the user object.

            If you have data from facebook which hast utf-8 encoded unicode strings,
            you need to use the following syntax: 'lastname': r'%s' % user['last_name']
        """

        newReceiver = {
                'email':user.email,
                'registered':time.mktime(datetime.datetime.now().timetuple()),
                'source':'API',
        }
        if attrs:
            attributes = [{'key': a, 'value': getattr(user, a)} for a in attrs]
            newReceiver['attributes'] = attributes,
        if activated:
            newReceiver['activated'] = time.mktime(datetime.datetime.now().timetuple())
        try:
            query = self.soap.service.receiverAdd(API_KEY, group_id, newReceiver)
        except WebFault, e:
            return e
        if sendmail and not activated:
            if not form_id:
                forms = self.get_forms(group_id)
                form_id = forms[0]['id']
            self.send_activation_mail(form_id, user.email)
        return query.data

    def deactivate_user(self, email, group_id):
        try:
            query = self.soap.service.receiverSetInactive(API_KEY, group_id, email)
        except WebFault, e:
            return e
        return query.data
