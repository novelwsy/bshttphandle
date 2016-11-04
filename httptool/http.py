import cookielib
import json
import urllib
import urllib2

from CustomHttpHandler import CustomHTTPHandler
from CustomHttpHandler import CustomHTTPSHandler
from CustomHttpProcessor import CustomHttpProcessor
from CustomRequest import CustomRequest

http_instance = None


class Http(object):
    def __init__(self):
        self.cookiejar = cookielib.CookieJar()
        self.processor = CustomHttpProcessor()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar), self.processor,
                                           CustomHTTPHandler(), CustomHTTPSHandler)
        self.baseUrl = None
        self._headers = {}
        self.timeout = 12000

    def getUrl(self, url):
        if url.startswith("http://") or url.startswith("https"):
            return url
        else:
            return self.baseUrl + url

    @staticmethod
    def url_encode(data):
        if data is None:
            return None
        if isinstance(data, dict):
            new_data = {}
            for key in data.keys():
                new_data[key] = data[key]
            return urllib.urlencode(new_data)
        return urllib.urlencode(data)

    def request(self, url, data={}, method="GET", content_type="application/x-www-form-urlencoded", headers={},
                callback=None):
        real_url = self.getUrl(url)
        send_data = None
        if content_type.lower().find("application/json") >= 0:
            if not isinstance(data, str):
                if isinstance(data, file):
                    send_data = data.read()
                    data.close()
                else:
                    send_data = json.dumps(data, separators=(',', ':')).encode('utf-8')
            else:
                send_data = data.encode('utf-8')
        else:
            if isinstance(data, file):
                send_data = data.read()
                data.close()
            elif isinstance(data, str):
                send_data = data
            else:

                send_data = self.url_encode(data)

        send_header = dict(headers)
        if (send_data is not None) and len(send_data) > 0 and method.lower() not in ['get']:
            send_header['Content-Type'] = content_type
            send_header['Content-Length'] = len(send_data)
        else:
            # get method ,url coding
            send_data = None
            if '?' in real_url:
                raise Exception()
            real_url = ''.join([real_url, '?', self.url_encode(data)])

        send_header['user-agent'] = 'http tool for ajax api.'
        send_header.update(self._headers)
        request = CustomRequest(real_url, send_data, send_header, method=method)
        response = self.opener.open(request, timeout=self.timeout)
        if callback is not None:
            callback(response)
        else:
            return response

    def addHeaders(self, headers):
        self._headers.update(headers)

    def get(self, url, data={}, contentType="text/html;charset=utf-8", header={}, callback=None):
        return self.request(url, data, "GET", contentType, header, callback)

    def post(self, url, data={}, contentType="application/x-www-form-urlencoded", header={}, callback=None):
        return self.request(url, data, "POST", contentType, header, callback)

    def put(self, url, data, contentType="application/json;charset=utf-8", header={}, callback=None):
        return self.request(self, url, "PUT", contentType, header, callback)

    def delete(self, url, data, contentType="application/json;charset=utf-8", header={}, callback=None):
        return self.request(url, data, 'DELETE', contentType, header, callback)

    def getJson(self, url, data={}, header={}, callback=None):
        reps = self.get(self, url, data, "application/json;charset=utf-8", header)
        return reps

    def postJson(self, url, data={}):
        return self.post(self, url, data, "application/json;charset=utf-8", header={}, callback=None)


def init_http():
    global http_instance
    if http_instance is None:
        http_instance = Http()
