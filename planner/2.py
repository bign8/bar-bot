"""
Dictionary copy became a problem with the first method of search

# Globals
0. Number of steps per circle
1. Number of Cups (indexed)
2. Number and sort order of ingredients (indexed)

Here define state as a string
- Each cups contentes can be described as a string
  - Based on the order of the ingredients Global(2)
  - each char will be the unicode codepoint
  - for whatever smallest deviation of measurement we have (half a fluid ounce?)
- cup contents are concatinated in cup order
- separater?
- rotation angle of system
  - ignore tau, split the full rotation into a # of divisions
- separator?
- the nozzle states (as bits - 1 and 0)

This way, the desired state of having all nozzles off can be used

Simplifying Assumptions:
- Ignore TAU and just pour when directly over glass
"""

import heapq
from itertools import chain, combinations


STEPS = 3
N_cups = 1

# The angle at which each cup is at
CUPS = [i / N_cups for i in range(N_cups)]
SPOUTS = [
    ("gin", 0),
    ("tonic", 1), # TODO: have these space out as we increase
    ("lime_juice", 2),
]

ACTIONS = ["step()"]
ACTIONS += ["pour(" + idx + ")" for idx in range(len(SPOUTS))]
ACTIONS += ["stop(" + idx + ")" for idx in range(len(SPOUTS))]

GandT = "\x02\x0D\x01" # Gin: 2, Tonic: 13, Lime: 1

# TODO: ignore stopping angle for goal
GOAL = GandT * N_cups + "?" + "000"
START = "\x00\x00\x00\x00000"

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def do(action, state):
    pass

queue = [START]
for state in queue:
    for action in ACTIONS:
        more = do(action, state)
        if more:
            queue.append(more)
