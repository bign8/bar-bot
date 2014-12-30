

class Rating(object):
    guid = None
    user = None
    rank = None
    stamp = None
    comment = None

    def __init__(self, **kwargs):
        extend(self, kwargs)
