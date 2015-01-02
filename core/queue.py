from Queue import *
from threading import Thread

_q = Queue()


def enqueue(fn, **kwargs):
    data = {
        'name': fn,
        'args': kwargs
    }
    _q.put_nowait(data)


def dequeue():
    data = None
    try:
        data = _q.get_nowait()
        _q.task_done()
    except Empty:
        pass

    return data


# def worker():
#     while True:
#         item = q.get()
#         print item
#         q.task_done()
#
# q = Queue()
# for i in range(4):
#     t = Thread(target=worker)
#     t.daemon = True
#     t.start()
#
# for item in xrange(10000):
#     q.put(item)
#
# print q.qsize()
#
# q.join()
#
# print 'done'
