import time
import getpass


def get_time():
    return time.strftime("%I:%M:%S %p", time.localtime())


def get_password():
    return getpass.getpass("What is your password?")