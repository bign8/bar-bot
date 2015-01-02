from threading import RLock
from threading import Semaphore

UNKNOWN_STATUS = 'unknown'
PENDING_STATUS = 'pending'
ACTIVE_STATUS = 'active'
COMPLETE_STATUS = 'complete'


class Order(object):
    _status = UNKNOWN_STATUS
    id = None
    listeners = None
    # TODO: more information about order

    def __init__(self):
        self.listeners = []

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        for listener in self.listeners:
            listener(value)
        self._status = value

    def add_listener(self, cb):
        self.listeners.append(cb)

    def rem_listener(self, cb):
        self.listeners.remove(cb)


class Orders(object):
    queue = None
    completed = None
    data = None
    lock = None
    semaphore = None

    def __init__(self):
        self.queue = []
        self.completed = []
        self.map = {}
        self.lock = RLock()
        self.semaphore = Semaphore(0)

    def place(self, order):
        """ WWW places order """
        idx = id(order)
        order.id = idx
        order.status = PENDING_STATUS

        with self.lock:
            if idx in self.map:
                raise Exception('Duplicate order')

            self.map[idx] = order
            self.queue.append(order)
            self.semaphore.release()

        return idx

    def has_next(self, blocking=False):
        """ PLC wait for next order (can block) """
        self.semaphore.acquire(blocking)

    def next(self):
        """ PLC gets order """
        with self.lock:
            order = self.queue.pop(0)
            order.status = ACTIVE_STATUS
        return order

    def complete(self, idx):
        """ PLC completes order """
        with self.lock:
            order = self.map[idx]
            order.status = COMPLETE_STATUS
            del self.map[idx]
