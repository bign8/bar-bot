"""
Drink Units: fluid ounces
"""

import math
import copy
from functools import partial
from itertools import chain, combinations

# http://stackoverflow.com/a/1482316/3220865
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

PI = math.pi
TAU = 2 * math.pi
R = 25 / 2 # 25" in diameter
R_SPOUT = 0.25 / 2
R_CUP = 4 / 2
N_cups = 1

# TODO: parse all this from environment
spouts = {
  "gin": 0,
  "tonic": TAU / 3,
  "lime_juice": 2 * TAU / 3,
}

# TODO: use better cup ID than this
cups = {i : i * TAU / N_cups for i in range(N_cups)}
goal = {i : {"gin": 2, "tonic": 13, "lime_juice": 1} for i in range(N_cups)}

# Adding all possible actions to the mix
actions = ["turn()"]
actions += ["pour({})".format(s) for s in spouts]
actions += ["stop({})".format(s) for s in spouts]

class Bot:
    def __init__(self):
        self.spouts_state = {key: False for key in spouts} # bool for each spout (is_pouring)
        self.cups_state = {key: {} for key in cups} # map of the various ingredient levels
        self.link = {} # map of spout -> cup
        self.time = 0
        self.angle = 0

        # Ignore when cloning
        self.slice = {} # actions performed in this time slice

    def __repr__(self):
        return "Bot(time: {}, angle: {}, spouts: {}, cups: {}, links: {})".format(self.time, self.angle, self.spouts_state, self.cups_state, self.link)

    # def perform(self, fns):
    #     """ Perform a set of actions on a given state """
    #     child = Bot()
    #     child.spouts_state = copy.deepcopy(self.spouts_state)
    #     child.cups_state = copy.deepcopy(self.cups_state)
    #     child.link = copy.deepcopy(self.link)
    #     child.time = self.time
    #     child.angle = self.angle
    #
    #     # Apply given actions to a state
    #     for fn in fns:
    #         if not getattr(child, fn[:4])(fn[5:-1]):
    #             return
    #
    #     return child.tock()

    def is_good(self, is_done=False):
        missed = False
        for cup_id, recipe in goal.iteritems():
            my_cup = self.cups_state[cup_id]
            for ingredient, amount in recipe.iteritems():
                if ingredient not in my_cup:
                    missed = True
                    continue
                if my_cup[ingredient] > amount:
                    return False
                if is_done and my_cup[ingredient] < amount:
                    return False
        if is_done:
            return not missed
        return True

    def apply(self, fn):
        """ Only works for 4 letter function names and with arguments wrapped in parens """
        return getattr(self, fn[:4])(fn[5:-1])

    def clone(self):
        bot = Bot()
        bot.spouts_state = copy.deepcopy(self.spouts_state)
        bot.cups_state = copy.deepcopy(self.cups_state)
        bot.link = copy.deepcopy(self.link)
        bot.time = self.time
        bot.angle = self.angle
        return bot

    def tock(self):
        """ The passage of time """
        self.time += 1
        if "turn()" in self.slice:
            self.angle += TAU / 6 # making things easy

        for ingredient, cup_id in self.link.iteritems():
            cup = self.cups_state[cup_id]
            if ingredient in cup:
                cup[ingredient] += 0.5
            else:
                cup[ingredient] = 0.5

        return self.is_good()

    def turn(self, _):
        """
        The planes are shifted with stepper motors.
        While the global design allows both planes to move independently,
          the only thing the planner needs are the angles relative to each other.
        """
        # check precondition (haven't already called this method)
        if "turn()" in self.slice:
            return False

        # TODO(in state validation): check precondition (pouring spouts will be over cups)

        # apply actions
        self.slice["turn()"] = True
        return True

    def pour(self, ingredient):
        """ Start pouring an ingredient """
        # check precondition (spout isn't already pouring)
        if ingredient in self.spouts_state and self.spouts_state[ingredient]:
            return False

        # check precondition (we have not just stopped pouring in this slice)
        if "stop(%s)".format(ingredient) in self.slice:
            return False

        # check precondition (spout is over cup)
        """
        1 = spout; 2 = cup
        a = angle; r = radius (no suffix = bot radius)
        p = pourable (spout is over cup)

        p = (x2 - x1) ** 2 + (y2 - y1) ** 2 < (r2 - r1) ** 2
        x2 = cos(a2) * r; x1 = cos(a1) * r
        (x2 - x1) = (cos(a2) - cos(a1)) * r

        dx, dy, dr = (cos(a1) - cos(a2)) * r, (sin(a1) - sin(a2)) * r, r2 - r1
        p = dx * dx + dy * dy < dr * dr
        """
        my_angle = self.angle + spouts[ingredient]
        my_x, my_y = math.cos(my_angle), math.sin(my_angle)
        dr = R_CUP - R_SPOUT

        def intersect(cup_angle):
            dx = (my_x - math.cos(cup_angle)) * R
            dy = (my_y - math.sin(cup_angle)) * R
            return dx * dx + dy * dy < dr * dr

        my_cup = None
        for cup_id, cup_angle in cups.iteritems():
            if intersect(cup_angle):
                my_cup = cup_id
                break
        if my_cup is None:
            return False

        # apply actions
        self.spouts_state[ingredient] = True
        self.link[ingredient] = my_cup
        self.slice["pour(%s)".format(ingredient)] = True
        return True

    def stop(self, ingredient):
        """ Stop pouring an ingredient """

        # check precondition (cup is pouring)
        if not self.spouts_state[ingredient]:
            return False

        # TODO: move to state validation - check precondition (we have not just started doing this action)
        if "pour(%s)".format(ingredient) in self.slice:
            return False

        # apply action (stop pouring)
        self.spouts_state[ingredient] = False
        del self.link[ingredient]
        self.slice["stop(%s)".format(ingredient)] = True
        return True

def distance(state):
    """ How many drink units are we from our goal? """
    total = 0
    for cup_id, recipe in goal.iteritems():
        cup = state.cups_state[cup_id]
        for ingredient, amount in recipe.iteritems():
            total += amount - cup[ingredient] if ingredient in cup else amount
    return total

"""
# Planning algorithm
- Iterate through all possible sets of actions (if a fn returns false, don't add to state set)
- call "tock" to create a new state
- repeat until goal state is reached

## branch limiting
- if an ingretient is ever more than the desired result, don't presue further
"""
if __name__ == "__main__":
    bot = Bot()

    # perform planning
    current = [bot]
    future = []

    while not current[0].is_good(True):
        state = current.pop()
        # print("The State", str(state))
        for fns in powerset(actions):
            if len(fns) is 0:
                continue

            # clone state
            clone = state.clone()

            # deterimin if actions are possible
            good = True
            for fn in fns:
                good = good and clone.apply(fn)
            good = good and clone.tock()
            if not good:  # bad state
                continue

            # if we are done, return
            if clone.is_good(True):
                print("TODO: return full state to get here", clone)
                import sys
                sys.exit(0)

            # otherwise add state to frontier
            current.append(clone)
        current = sorted(current, key=distance, reverse=True)

    # print("cups:", cups)
    # print("goal:", goal)