from http import http_instance


def HttpSession(url, method="GET", data={}, contentType="application/x-www-form-urlencoded", header={}):
    def wrapper(func):
        def wrapper_func():
            ret = None
            try:
                rep = http_instance.request(url, data, method, contentType, header)
                ret = func(rep)
                rep.close()
            except Exception, e:
                print(e)
                raise e
            return ret

        return wrapper_func

    return wrapper
