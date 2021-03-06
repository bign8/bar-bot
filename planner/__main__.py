"""
Drink Units: fluid ounces
"""

import math
import heapq
from itertools import chain, combinations

# http://stackoverflow.com/a/1482316/3220865
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

PI = math.pi
TAU = 2 * math.pi
R = 25.0 / 2 # 25" in diameter
R_SPOUT = 0.25 / 2
R_CUP = 4.0 / 2
N_cups = 3
DR = TAU / (3 * 10) # making things easy

# TODO: simplify math because of radius divisions and such
# https://en.wikipedia.org/wiki/Circular_segment
cup_theta = 2 * math.asin(R_CUP / (R * 2))
spout_theta = 2 * math.asin(R_SPOUT / (R * 2))
dt = cup_theta - spout_theta

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

    dx = (math.cos(my_angle) - math.cos(cup_angle)) * R
    dy = (math.sin(my_angle) - math.sin(cup_angle)) * R
    resA = dx * dx + dy * dy < (R_CUP - R_SPOUT) ** 2

    # NEW WAY!!!
    https://en.wikipedia.org/wiki/Circular_segment
    angle delta = 2 * arcsin(c / (2*R))
    """
    a = my_angle - cup_angle
    if a < 0:
        a = -a
    a %= TAU
    return a < dt if a <= PI else TAU - a < dt

# Precompute some intersect logic
lookup = {} # angle -> cup_id
my_angle = 0
while my_angle < TAU + DR/2:
    tmp_angle = round(my_angle, 4)
    for cup_id, cup_angle in cups.iteritems():
        if intersect(tmp_angle, cup_angle):
            lookup[tmp_angle] = cup_id
            break
    my_angle += DR

class Bot:
    def __init__(self, ss=None, cs=None):
        self.spouts_state = ss if ss else {key: False for key in spouts} # bool for each spout (is_pouring)
        self.cups_state = cs if cs else {key: {} for key in cups} # map of the various ingredient levels
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
        """
        Only works for 4 letter function names and with arguments wrapped in parens
        The following is faster than `getattr(self, fn[:4])(fn[5:-1])`
        """
        return {"t": self.turn, "p": self.pour, "s": self.stop}[fn[0]](fn[5:-1])

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
        bot = Bot(
            ss=dict(self.spouts_state),
            cs={key: dict(value) for key, value in self.cups_state.iteritems()},
        )
        bot.link = dict(self.link)
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
        if "stop(" + ingredient + ")" in self.actions:
            return False

        # check precondition (spout is over cup)
        my_cup = self.get_pour_cup(self.angle + spouts[ingredient])
        if my_cup is None:
            return False

        # apply actions
        self.spouts_state[ingredient] = True
        self.link[ingredient] = my_cup
        return True

    def get_pour_cup(self, my_angle):
        """
        original (lookup is just pre-computed)
        for cup_id, cup_angle in cups.iteritems():
            if intersect(my_angle, cup_angle):
                return cup_id
        """
        tmp_angle = round(my_angle % TAU, 4)
        return lookup[tmp_angle] if tmp_angle in lookup else None

    def stop(self, ingredient):
        """ Stop pouring an ingredient """

        # check precondition (cup is pouring)
        if not self.spouts_state[ingredient]:
            return False

        # check precondition (we have not just started doing this action)
        if "pour(" + ingredient + ")" in self.actions:
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

class BotList:
    """ An ordered list that uses a heap to maintain order """
    def __init__(self, key):
        self.key = key
        self.heap = [tuple([1e9, Bot()])]

    def __iter__(self):
        while bool(self.heap[0][0]): # iff the distance is 0, we are done!
            yield self.pop()

    def pop(self):
        return heapq.heappop(self.heap)[1]

    def insert(self, bot):
        heapq.heappush(self.heap, tuple([self.key(bot), bot]))

"""
# Planning algorithm
- Iterate through all possible sets of actions (if a fn returns false, don't add to state set)
- call "tock" to create a new state
- repeat until goal state is reached

## branch limiting
- if an ingretient is ever more than the desired result, don't presue further
"""
if __name__ == "__main__":
    evals = 0
    queue = BotList(key=distance)
    for state in queue:
        # print("State", state)
        for fns in powerset(actions):
            evals += 1
            clone = state.clone()  # clone state
            if not clone.perform(fns):  # determine if actions are possible
                continue
            # TODO: if clone.is_good(True): return clone
            queue.insert(clone)

    print("Evaluated", evals, len(queue.heap))

    # State is found
    answer = []
    state = queue.pop()
    while state.parent:
        answer.append(tuple([state.actions, state]))
        state = state.parent

    # Reporting the plan!
    for i, step in enumerate(reversed(answer)):
        print("Step {}: {}".format(i, step))
    print("TODO: figure out how to shut things off")
