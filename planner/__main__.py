"""
Drink Units: fluid ounces
"""

import math
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
actions = ["tick()"]
actions += ["pour(%s)".format(s) for s in spouts]
actions += ["stop(%s)".format(s) for s in spouts]

class Bot:
    def __init__(self):
        self.spouts = spouts # angle offset for each spout
        self.spouts_state = {key: False for key in self.spouts} # bool for each spout (is_pouring)

        self.cups = cups # angle offset for each cup
        self.cups_state = {key: {} for key in self.cups} # map of the various ingredient levels

        self.link = {} # map of spout -> cup

        # Keeping track of the actions
        self.time = 0
        self.angle = 0
        self.slice = {} # actions performed in this time slice
        self.actions = [self.tick]
        self.actions += [partial(self.pour, key) for key in self.spouts]
        self.actions += [partial(self.stop, key) for key in self.spouts]

    def tock(self):
        """ The passage of time """
        if "tick()" in self.slice:
            self.angle += TAU / 6 # making things easy

        for ingredient, cup_id in self.link:
            cup = self.cups_state[cup_id]
            if ingredient in cup:
                cup[ingredient] += 0.5
            else:
                cup[ingredient] = 0.5

    def tick(self):
        """
        The planes are shifted with stepper motors.
        While the global design allows both planes to move independently,
          the only thing the planner needs are the angles relative to each other.
        """
        # check precondition (haven't already called this method)
        if "tick()" in self.slice:
            return False

        # TODO: check precondition (pouring spouts will be over cups)

        # apply actions
        self.slice["tick()"] = True

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
        my_angle = self.angle + self.spouts[ingredient]
        my_x, my_y = math.cos(my_angle), math.sin(my_angle)
        dr = R_CUP - R_SPOUT

        def intersect(cup_angle):
            dx = (my_x - math.cos(cup_angle)) * R
            dy = (my_y - math.sin(cup_angle)) * R
            return dx * dx + dy * dy < dr * dr

        my_cup = None
        for cup_id, cup_angle in self.cups.iteritems():
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

        # check precondition (we have not just started doing this action)
        if "pour(%s)".format(ingredient) in self.slice:
            return False

        # apply action (stop pouring)
        self.spouts_state[ingredient] = False
        del self.link[ingredient]
        self.slice["stop(%s)".format(ingredient)] = True
        return True

"""
# Planning algorithm
- Iterate through all possible sets of actions (if a fn returns false, don't add to state set)
- call "tock" to create a new state
- repeat until goal state is reached

## branch limiting
- if an ingreatient is ever more than the desired result, don't presue further
"""
if __name__ == "__main__":
    bot = Bot()

    # # Testing actions
    # print(self.actions[1]()) # start pouring 1
    # print(self.actions[4]()) # stop pouring 1

    # perform planning
    current = [bot]
    future = []

    for state in current:
        for fns in powerset(range(len(state.actions))):
            # determine if actions are possible (continue if not)
            # apply actions to state
            # check if new state exceedes conditions (continue if so)
            # check if new state meets condiitons (return plan if so)
            # add state to future
            pass

    print("cups:", cups)
    print("goal:", goal)
