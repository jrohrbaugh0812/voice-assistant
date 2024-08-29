import time


def get_time():
    return time.strftime("%I:%M:%S %p", time.localtime())

