from recognizer import recognize_speech
from responder import respond
import keyboard

if __name__ == "__main__":
    print("Voice Assistant Started")
    text = 'something'
    while text:
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("shift") and keyboard.is_pressed("space"):
            text = input("Input: ")
            if text:
                respond(text)

