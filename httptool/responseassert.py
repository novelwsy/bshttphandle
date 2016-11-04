# -*- coding: utf-8 -*-
import json
import urllib2

ast = None


class ResponseAssert(object):
    def __init__(self):
        super(ResponseAssert, self).__init__()

    def tojson(self, s):
        try:
            if isinstance(s, str):
                return json.loads(s)
            if isinstance(s, urllib2.addinfourl):
                return json.loads(s.read())
        except Exception, e:
            raise e

    def doAssert(self, response, callback=None):
        data = None
        orgData = response.read()
        conenttype = response.headers.getheader("content-type").lower()
        if conenttype.find("application/json") >= 0:
            data = self.tojson(orgData)
        else:
            data = orgData
        if (callback != None):
            return (callback(response, data), data)

    def contains(self, req, containStr):
        return self.doAssert(req, lambda req, content: content.find(containStr) >= 0)

    def isRestOk(self, req):
        return self.doAssert(req, lambda req, content: content['code'] == 200)

    def isRestError(self, req):
        return self.doAssert(req, lambda req, content: content['code'] == 500)

    def isHttpCode(self, req, code):
        return req.code == code

    def hasHeader(self, req, name, value):
        return self.doAssert(req, lambda req, content: req.headers.getheader(name) == value)

    def dump(self, req, fileName):
        content = req.read()
        f = open(fileName, 'w')
        f.write(content)
        f.close()


def init_assert():
    global ast
    if ast is None:
        ast = ResponseAssert()
