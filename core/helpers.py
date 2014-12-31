from __future__ import division
from math import pi, floor


def radian_wrap(value):
    pi2 = 2 * pi
    return value - pi2 * floor((value + pi) / pi2)


def diff_radians(current, target):
    return radian_wrap(target - current)
