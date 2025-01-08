import pyttsx3
import time
from getpass import getpass


def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_time():
    return time.strftime("%I:%M:%S %p", time.localtime())


def get_password():
    return getpass("What is your password? ")
