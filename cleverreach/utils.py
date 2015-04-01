# coding: utf-8
"""
Helper functions for Django.
"""

__all__ = ['insert_new_user',]

import datetime, time

from api.v5_1 import Client

class User(object):
    """ Bunch class for converting a dict into an object. """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k not in self.__dict__:
                self.__dict__[k] = v



def insert_new_user(user, list_id, activated=None, sendmail=True,
                        form_id=None, attrs=None, client=None):
    """
    Adds a new single receiver. If the email address already exists, an error is raised.

    Keyword arguments:

    * user --  Can be a dict (such as cleaned_data) or an object (such as request.user).
    * list_id -- The receiver group id
    * activated -- (True/False) If the new address is already activated or not (double opt-in).
        If activated is not set or None, the cleverreach default settings are used.
    * sendmail -- boolean, if True, an activation email will be sent out by cleverreach.
    * form_id -- (optional) The id of the form used for the list. If this is not
        provided, the first available form is used.
    * attrs -- (optional) This needs to be a list in the form ['first_name', 'last_name'] and
        the attribute must exist on the user object/dict.
    * client -- (optional) If an instance of the api.Client exists already, you can
        pass it to the function. Otherwise a new instance is created.
    """

    if type(user) == dict:
        user = User(**user)

    if not isinstance(client, Client):
        client = Client()

    newReceiver = {
            'email':user.email,
            'registered':time.mktime(datetime.datetime.now().timetuple()),
            'source':'API',
    }
    if attrs:
        attributes = [{'key': a, 'value': getattr(user, a)} for a in attrs]
        newReceiver['attributes'] = attributes

    if type(activated) == bool:
        if activated:
            newReceiver['activated'] = time.mktime(
                datetime.datetime.now().timetuple())
        else:
            newReceiver['deactivated'] = time.mktime(
                datetime.datetime.now().timetuple())
    elif type(activated) == datetime.datetime:
        newReceiver['activated'] = time.mktime(activated.timetuple())
    elif type(activated == float):  # assume timetuple
        newReceiver['activated'] = activated


    data = client.receiver_add(list_id, newReceiver)

    if sendmail and not data.active:
        if not form_id:
            forms = client.forms_get_list(list_id)
            form_id = forms[0]['id']
        client.forms_activation_mail(form_id=form_id, email=user.email)
    return data
