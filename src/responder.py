import pyttsx3
from intents import get_intent
from utils import get_time


def respond(user_text):
    user_text = user_text.lower()
    intent = get_intent(user_text)

    if intent == "greeting":
        response = "Hello, how are you?"
    elif intent == "time_query":
        response = "The time is: " + get_time()
    else:
        response = "I'm not sure how to respond to that."
    print(response)
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()
