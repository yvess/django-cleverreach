# coding: utf-8

"""
You have to define a group (in the cleverreach admin panel) for each language.
The form code is optional, we use the first form if it is not provided.

The Cleverreach API requires suds: https://fedorahosted.org/suds/

You have to define the following parameters in your settings.py:

    CLEVERREACH = {'api_key': '<API KEY>',}

API documentation is at http://api.cleverreach.com/soap/doc/5.0/

"""

import logging

from django.conf import settings

from suds.client import Client as SudsClient
from suds import WebFault

from cleverreach import CleverreachAPIException

logger = logging.getLogger('cleverreach.api')


URL = 'http://api.cleverreach.com/soap/interface_v5.1.php?wsdl'
API_KEY = settings.CLEVERREACH.get('api_key')


class Client(object):

    def __init__(self):
        self.soap = SudsClient(URL)  #immediately opens up a connection.
        self.raise_exceptions = settings.CLEVERREACH.get('raise_exceptions', True)

    # TODO: dotted path helper

    def query_data(self, method, *args, **kwargs):
        try:
            response = getattr(self.soap.service, method)(API_KEY, *args, **kwargs)
        except WebFault as e:
            if self.raise_exceptions:
                raise e
            else:
                logger.error(e)
                return response.data
        else:
            if response.status == "ERROR":
                if self.raise_exceptions:
                    message = u'Error for method %s: %s. Data: %s' % \
                              (method, response.message, response.data)
                    raise CleverreachAPIException(message, response.statuscode)
                else:
                    logger.error(response.message)

        return response.data

    # Client


    # Group

    def group_get_list(self):
        """
        Returns a list of group classes of the form:
        (group){
           id = 108907
           name = "test1"
           last_mailing = 1335887342
           last_changed = 1335886187
           count = 84
           inactive_count = 0
           total_count = 84
         }
        The dict keys are actually object properties.
        """
        return self.query_data('groupGetList')

    def group_clear(self, list_id):
        """
        truncates the contents of a the Group

        Warning: This may have heavy impact on statistics and campaigns
        since every related data (receivers, orders, events) will removed.
        """
        return self.query_data('groupClear', list_id)


    # Forms

    def forms_get_list(self, list_id):
        """
        Returns a list of available forms for the given group.
        Forms are object with the properties [id, name, description]
        """
        return self.query_data('formsGetList', list_id)

    def forms_get_code(self, form_id):
        """
        Returns the HTML code for the given embedded form.
        @param form_id: the id of the form (not the list!)
        """
        return self.query_data('formsGetCode', form_id)

    def forms_activation_mail(self, form_id, email, doidata=None):
        """
        Will send the activation mail to the given email.
        You will have to manualy add the receiver first with "receiver.add"
        or use an existing one.
        If the user allready is activated, status will return an error.
        """
        if not doidata:
            doidata = {'user_ip': '127.0.0.1', 'user_agent': 'mozilla',
                       'referer': 'http://www.gotham.com/newsletter_subscribe/',
                       'postdata': 'firtsname:bruce,lastname:whayne,nickname:Batman',
                       'info': 'Extra info. the more you provide, the better.'}

        return self.query_data('formsSendActivationMail', form_id, email, doidata)

    # Mailing

    # Receiver

    def receiver_add(self, list_id, receiver):
        """
        Adds a new single receiver

        This function tries to add a single receiver.
        If the receiver allready exists, the operation will Fail.
        Use receiver_update in that case.
        The default form only accepts email, registered, activated,
        source and attributes.
        To add more fields you have to add them as attributes. Make sure the keys
        are the same as the name of the fields in the form. (Check with get_by_email)
        Attribute keys may only contain lowercase a-z and 0-9.

        """
        return self.query_data('receiverAdd', list_id, receiver)

    def receiver_get_by_email(self, list_id, email, level=1):
        """
        Gets userdetails based on given readout level.
        Possible levels (bit whise).
        000 (0) > Basic readout with (de)activation dates
        001 (1) > including attributes (if available)
        010 (2) > including Events (if available)
        100 (4) > including Orders (if available)
        """
        return self.query_data('receiverGetByEmail', list_id, email, level)

    def receiver_set_active(self, list_id, email):
        """
        Deactivates a given receiver/email
        The receiver wont receive anymore mailings from the system.
        This sets/overwrites the deactivation date with the current date.
        """
        return self.query_data('receiverSetActive', list_id, email)

    def receiver_set_inactive(self, list_id, email):
        """
        Deactivates a given receiver/email
        The receiver wont receive anymore mailings from the system.
        This sets/overwrites the deactivation date with the current date.
        """
        return self.query_data('receiverSetInactive', list_id, email)
