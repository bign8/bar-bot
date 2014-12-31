from ui import Drawable
from math import cos, sin
from helpers import radian_wrap


class Plane(Drawable):
    _angle = 0
    targets = None

    def __init__(self, angle=0, targets=[]):
        super(Plane, self).__init__()
        self.angle = angle
        self.targets = targets

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = radian_wrap(value)

    def setup(self, graphics, win):
        radius = 200
        center = graphics.Point(300, 300)
        lend = graphics.Point(350, 300)

        circle = graphics.Circle(center, radius)
        circle.setOutline('black')
        circle.draw(win)

        line = graphics.Line(center, lend)
        line.setOutline('red')
        line.setArrow('last')
        line.draw(win)

        self.g_vars = {
            'line': line,
            'radius': 50,
            'center': center
        }

    def draw(self, win):
        radius = self.g_vars['radius']
        center = self.g_vars['center']
        old_line = self.g_vars['line']

        old_line.undraw()
        new_line = old_line.clone()

        new_line.p2 = center.clone()
        new_line.p2.x += radius * cos(self.angle)
        new_line.p2.y += radius * sin(self.angle)
        new_line.draw(win)

        self.g_vars['line'] = new_line

    def update(self):
        self.angle += 0.033
