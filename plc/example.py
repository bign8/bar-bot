__author__ = 'bign8'

"""
Basic logic wireframe for PLC

"""

class WebServer(object):

    def __init__(self):
        pass

    def get_data(self, name):
        pass

    def set_data(self, name, value):
        pass

class Application(object):

    @classmethod
    def main(cls):
        me = cls()
        while True:
            me.update()
            me.loop()

    def __init__(self):
        # parse hardware configuration constants
        # load persistant storage about fluid levels + users
        # initialize web server (input + output device)
        self.web = WebServer()
        # initialize motor drivers (output device)
        # setup position sensors
        # zero system out

        self.top_angle = 0
        self.bot_angle = 0

    def update(self):
        pass

    def loop(self):
        pass



if __self__ == '__main__':
    Application.main()
