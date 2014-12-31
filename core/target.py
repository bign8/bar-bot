from __future__ import division
from helpers import radian_wrap


class Target(object):
    active = False
    amount = 0.0
    capacity = 0.0
    _start = 0.0
    _stop = 0.0

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def draw(self):
        pass

    @property
    def percent(self):
        return self.amount / self.capacity

    # start
    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = radian_wrap(start)

    # stop
    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, stop):
        self._stop = radian_wrap(stop)


