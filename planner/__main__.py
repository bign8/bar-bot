"""
Drink Units: fluid ounces
"""

import math
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
DR = TAU / (3 * 8) # making things easy

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

def intersect(my_angle, cup_angle):
    """
    Does my robots angle intersect wiht my cup!

    1 = spout; 2 = cup
    a = angle; r = radius (no suffix = bot radius)
    p = pourable (spout is over cup)

    p = (x2 - x1) ** 2 + (y2 - y1) ** 2 < (r2 - r1) ** 2
    x2 = cos(a2) * r; x1 = cos(a1) * r
    (x2 - x1) = (cos(a2) - cos(a1)) * r

    dx, dy, dr = (cos(a1) - cos(a2)) * r, (sin(a1) - sin(a2)) * r, r2 - r1
    p = dx * dx + dy * dy < dr * dr
    """
    dx = (math.cos(my_angle) - math.cos(cup_angle)) * R
    dy = (math.sin(my_angle) - math.sin(cup_angle)) * R
    return dx * dx + dy * dy < (R_CUP - R_SPOUT) ** 2

class Bot:
    def __init__(self):
        self.spouts_state = {key: False for key in spouts} # bool for each spout (is_pouring)
        self.cups_state = {key: {} for key in cups} # map of the various ingredient levels
        self.link = {} # map of spout -> cup
        self.angle = 0
        self.parent = None
        self.actions = None # Ignore when cloning, set by perform

    def __repr__(self):
        return "Bot(angle: {}, spouts: {}, cups: {}, links: {})".format(
            self.angle, self.spouts_state, self.cups_state, self.link)

    def perform(self, fns):
        """ Perform a set of actions on a given state """
        self.actions = fns
        for fn in fns:
            if not self.apply(fn):
                return
        return self.tock()

    def apply(self, fn):
        """ Only works for 4 letter function names and with arguments wrapped in parens """
        return getattr(self, fn[:4])(fn[5:-1])

    def is_good(self, is_done=False):
        """ Are we in a good state (ingriedients less than or equal to the desired amounts) """
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

    def clone(self):
        bot = Bot()
        bot.cups_state = {key: value.copy() for key, value in self.cups_state.iteritems()}
        bot.spouts_state = self.spouts_state.copy()
        bot.link = self.link.copy()
        bot.angle = self.angle
        bot.parent = self
        return bot

    def tock(self):
        """ The passage of time """
        if "turn()" in self.actions:
            self.angle += DR

            # check postcondition (assert we are still pouring into cups)
            for spout, cup_id in self.link.iteritems():
                if not intersect(self.angle, cups[cup_id]):
                    return False

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
        # TODO(in state validation): check precondition (pouring spouts will be over cups)
        return True

    def pour(self, ingredient):
        """ Start pouring an ingredient """
        # check precondition (spout isn't already pouring)
        if ingredient in self.spouts_state and self.spouts_state[ingredient]:
            return False

        # check precondition (we have not just stopped pouring in this slice)
        if "stop({})".format(ingredient) in self.actions:
            return False

        # check precondition (spout is over cup)
        my_angle = self.angle + spouts[ingredient]
        my_cup = None
        for cup_id, cup_angle in cups.iteritems():
            if intersect(my_angle, cup_angle):
                my_cup = cup_id
                break
        if my_cup is None:
            return False

        # apply actions
        self.spouts_state[ingredient] = True
        self.link[ingredient] = my_cup
        return True

    def stop(self, ingredient):
        """ Stop pouring an ingredient """

        # check precondition (cup is pouring)
        if not self.spouts_state[ingredient]:
            return False

        # check precondition (we have not just started doing this action)
        if "pour({})".format(ingredient) in self.actions:
            return False

        # apply action (stop pouring)
        self.spouts_state[ingredient] = False
        del self.link[ingredient]
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
    current = [Bot()]
    while not current[0].is_good(True):
        state = current.pop(0)
        for fns in powerset(actions):
            clone = state.clone()  # clone state
            if not clone.perform(fns):  # determine if actions are possible
                continue
            # TODO: if clone.is_good(True): return clone
            current.append(clone)  # Add state to the current set to be evaluated
        current = sorted(current, key=distance)

    # State is found
    answer = []
    state = current.pop(0)
    while state.parent:
        answer.append(tuple([state.actions, state]))
        state = state.parent

    # Reporting the plan!
    for i, step in enumerate(reversed(answer)):
        print("Step {}: {}".format(i, step))
    print("TODO: figure out how to shut things off")
