import pyttsx3
import random
import tkinter as tk
from tkinter.filedialog import askopenfilename
import webbrowser
from intents import get_intent
from utils import get_time


def greet():
    greetings = ["Hello, how are you?", "Hi, what are you doing?", "Hello, what do you need help with?",
                 "Hello, what can I do for you?"]
    return random.choice(greetings)


def tell_time():
    return "The time is: " + get_time()


def open_default_browser():
    url = "https://google.com"
    webbrowser.open(url)
    return "Your default browser has been opened."


def open_file_explorer():
    tk.Tk().withdraw()

    fn = askopenfilename()
    return "user chose" + fn


COMMANDS = {
    "greeting": greet,
    "time_query": tell_time,
    "browser": open_default_browser,
    "file_explorer": open_file_explorer,
}


def respond(user_text):
    user_text = user_text.lower()
    intent = get_intent(user_text)
    response = COMMANDS.get(intent, lambda: "I'm not sure how to respond to that.")()
    print(response)
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()
