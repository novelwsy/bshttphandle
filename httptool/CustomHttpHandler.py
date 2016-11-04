import urllib2

from CustomHttpConnection import CustomHTTPConnection
from CustomHttpConnection import CustomHTTPSConnection


class CustomHTTPHandler(urllib2.HTTPHandler):
    def http_open(self, req):
        return self.do_open(CustomHTTPConnection, req)


class CustomHTTPSHandler(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(CustomHTTPSConnection, req)
