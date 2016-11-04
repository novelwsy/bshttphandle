import urllib2


class CustomRequest(urllib2.Request):
    def __init__(self, *args, **kwargs):
        self._method = kwargs.pop('method', None)
        self._referer = kwargs.pop('referer', None)
        urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self):
        return self._method
