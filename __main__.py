from www import main as www
from plc import main as plc
from threading import Thread
from helpers import ThreadSafeDict


# Main order queue to run between server
orders = ThreadSafeDict()


def main():
    args = [orders]

    # start web server
    server = Thread(target=www, args=args)
    server.daemon = True
    server.start()

    # start plc
    robot = Thread(target=plc, args=args)
    robot.daemon = True
    server.start()

    # wait to kill children
    server.join()
    robot.join()


if __name__ == '__main__':
    main()
