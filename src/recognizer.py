import speech_recognition as sr
import random


def fallback_response():
    return random.choice([
        "Sorry, I didn't understand that.",
        "Could you rephrase?",
        "I'm not sure I can help with that."
    ])


def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text

    except sr.UnknownValueError:
        print(fallback_response())
    except sr.RequestError:
        print("Sorry, there was an error with the request.")
    return None
