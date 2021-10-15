import threading
import queue
import time
import logging


queue = queue.Queue()
logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def test(queue):
    while True:
        logging.debug("test")
        queue.put(input())
        time.sleep(1)

def test2(queue):
    while True:
        logging.debug("test")
        logging.debug(queue.get())


t1 = threading.Thread(target=test, args=(queue, ))
t2 = threading.Thread(target=test, args=(queue, ))
t1.start()
t2.start()
