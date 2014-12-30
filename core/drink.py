from __future__ import division
from .rating import Rating


class Drink(object):
    name = ''
    cost = 0
    parts = set()
    count = set()
    labels = set()  # strings
    ratings = set()

    @property
    def rating(self):
        values = [rating.value for rating in self.ratings]
        total = len(values)
        return values / total, total

    def vote(self, **kwargs):
        val = Rating(**kwargs)
        rating.add(val)
