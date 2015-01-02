from www import main as www_main
from plc import main as plc_main
from threading import Thread
from core.orders import Orders


# Main order queue to run between server
orders = Orders()


def main():
    args = [orders]

    # start web server
    server = Thread(target=www_main, args=args)
    server.daemon = True
    server.start()

    # start plc
    robot = Thread(target=plc_main, args=args)
    robot.daemon = True
    server.start()

    # wait to kill children
    server.join()
    robot.join()


if __name__ == '__main__':
    main()
