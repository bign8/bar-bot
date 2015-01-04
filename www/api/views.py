from www.decorators import json


@json
def index(request):
    return {'user': 'two'}


