from recognizer import recognize_speech
from responder import respond


if __name__ == "__main__":
    print("Voice Assistant Started")
    text = recognize_speech()
    if text:
        respond(text)
