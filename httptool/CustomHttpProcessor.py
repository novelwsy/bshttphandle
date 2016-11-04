import urllib2


class CustomHttpProcessor(urllib2.BaseHandler):
    def __init__(self):
        pass

    def http_request(self, request):
        return request

    def http_response(self, request, response):
        return response

    https_request = http_request
    https_response = http_response
