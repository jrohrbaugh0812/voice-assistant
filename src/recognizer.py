import speech_recognition as sr
import random


def fallback_response():
    return random.choice([
        "Sorry, I didn't understand that.",
        "Could you rephrase?",
        "I'm not sure I can help with that."
    ])


def _capture_speech(prompt="Listening...", timeout=3, phrase_time_limit=5):
    # Helper function to capture speech with customization.
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print(prompt)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("Processing audio...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print(f"Request error: {e}")
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
    return None


def recognize_speech():
    # Default speech recognizer for general commands.
    return _capture_speech(prompt="Listening...")


def recognize_save_note():
    # Specialized speech recognizer for saving notes.
    return _capture_speech(prompt="What would you like to save?", timeout=5, phrase_time_limit=10)
