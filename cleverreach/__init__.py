# version reflects cleverreach API version used.
VERSION = (5, 1, 0)
__version__ = '.'.join(map(str, VERSION))

class CleverreachAPIException(Exception):
    def __init__(self, message, statuscode=None):
        super(CleverreachAPIException, self).__init__(message)
        self.statuscode = statuscode

    def __unicode__(self):
        return unicode(self.message)

