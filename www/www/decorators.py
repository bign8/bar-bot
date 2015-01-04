from django.http import HttpResponse
from json import dumps


def json(fn):
    def wrapper(*args, **kwargs):
        obj = fn(*args, **kwargs)
        return HttpResponse(
            dumps(obj, sort_keys=True, indent=4),
            content_type='application/json'
        )
    return wrapper
