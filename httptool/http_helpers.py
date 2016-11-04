import json
import time


def timing():
    def wrapper(func):
        def wrapper_func(*args, **kwargs):
            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                end = time.time()
                print('%s:%s' % (func.func_name, end - start))

        return wrapper_func

    return wrapper


def to_json(encoding='utf-8'):
    def wrapper(func):
        def wrapper_func(*args, **kwargs):
            response = func(*args, **kwargs)
            if response.code == 200 and 'json' in response.headers.type:
                return json.load(response, encoding)
            return response.read()

        return wrapper_func

    return wrapper
