from threading import RLock


def _lock_it(self, name):
    def wrapped(*args, **kwargs):
        with self.status_lock:
            parent = super(ThreadSafeDict, self)
            fn = getattr(parent, name)
            data = fn(*args, **kwargs)
        return data

    return wrapped


# Thread safe dict
class ThreadSafeDict(dict):
    status_lock = None

    def __init__(self, *args, **kwargs):
        super(ThreadSafeDict, self).__init__(*args, **kwargs)
        self.status_lock = RLock()

        methods = dir(dict)
        methods.remove('__init__')

        for method in methods:
            setattr(self, method, _lock_it(self, method))
    #
    # def __setitem__(self, key, value):
    #     with self.status_lock:
    #         super(ThreadSafeDict, self).__setitem__(key, value)
    #
    # def __getitem__(self, item):
    #     with self.status_lock:
    #         data = super(ThreadSafeDict, self).__getitem__(item)
    #     return data
    #
    # def __delitem__(self, key):
    #     with self.status_lock:
    #         super(ThreadSafeDict, self).__delitem__(key)
