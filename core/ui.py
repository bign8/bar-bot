import graphics as g
from time import sleep


class Drawable(object):
    items = []

    def __init__(self, to_include=True):
        if to_include:
            self.items.append(self)
        self.g_vars = {}

    def setup(self, graphics, window):
        return None

    def draw(self, window):
        pass

    def update(self):
        pass


class UI(object):
    win = None

    def __init__(self):
        self.win = g.GraphWin('Test', 600, 600, False)

    def __call__(self):
        self.setup()

        try:
            while self.win.isOpen():
                self.draw()
                self.win.update()
                sleep(0.02)
        except KeyboardInterrupt:
            pass

    def setup(self):
        for item in Drawable.items:
            item.setup(g, self.win)

    def draw(self):
        for item in Drawable.items:
            item.update()
            item.draw(self.win)

    @staticmethod
    def gen_key(item):
        return str(id(item))
