from plane import Plane
from math import copysign
from helpers import diff_radians


class Bot(object):
    top = None
    bot = None

    def __init__(self):
        self.top = Plane()
        self.bot = Plane()

    def update(self):

        # TODO: do this based off of viscosity of the liquid
        amount = 0.033

        # clear all targets
        for target in (self.top.targets + self.bot.targets):
            target.active = False

        # set active on targets
        for top in self.top.targets:
            for bot in self.bot.targets:
                start_diff = diff_radians(top.start, bot.start)
                stop_diff = diff_radians(top.stop, bot.stop)

                is_active = copysign(1, start_diff) != copysign(1, stop_diff)
                is_active &= bot.ammout < bot.capacity
                is_active &= top.amount > 0

                if is_active:
                    top.amount -= amount
                    bot.amount += amount

                    top.active |= is_active
                    bot.active |= is_active
