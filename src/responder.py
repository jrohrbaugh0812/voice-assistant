import pyttsx3
import random
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
import webbrowser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from intents import get_intent
from recognizer import (recognize_save_note, recognize_sender_email_address, recognize_email_password,
                        recognize_receiver_email_address, recognize_email_body, recognize_email_subject)
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
    file_path = askopenfilename()  # Open file dialog
    if file_path:
        os.startfile(file_path)  # Open the selected file
        return f"Opening file: {file_path}"
    else:
        return "No file was selected."


def save_note():
    note = recognize_save_note()
    file = open("my_notes.txt", "w")
    file.write(note + "\n")
    file.close()
    return "Your note has been saved in \"my_notes.txt\""


def send_email():
    sender_email_address = input("What is your email address?")
    password = input("What is your password")
    receiver_email_address = input("What is the email address you want to contact?")
    input_type = input("Do you want to type OR speak the subject and body contents?")
    if input_type == "type":
        email_subject = input("What would you like the subject of the email to be?")
        email_body = input("What would you like the body of the email to be?")
    elif input_type == "speak":
        email_subject = recognize_email_subject()
        email_body = recognize_email_body()
    else:
        return "Invalid input type"

    msg = MIMEMultipart()
    msg["From"] = sender_email_address
    msg["To"] = receiver_email_address
    msg["Subject"] = email_subject
    msg.attach(MIMEText(email_body, "plain"))

    # Sending the email (i.e., "msg")
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email_address, password)  # Login to the server
            server.sendmail(sender_email_address, receiver_email_address, msg.as_string())  # Send email
            return "Email sent successfully."
    except Exception as e:
        return f"An error occurred: {e}"


def quit_program():
    regards = ["Goodbye, have a nice day!", "Have a good day!", "Bye, have a great day!"]
    return random.choice(regards)


COMMANDS = {
    "greeting": greet,
    "time_query": tell_time,
    "browser": open_default_browser,
    "file_explorer": open_file_explorer,
    "note": save_note,
    "email": send_email,
    "end": quit_program,
}


def respond(user_text):
    user_text = user_text.lower()
    intent = get_intent(user_text)
    response = COMMANDS.get(intent, lambda: "I'm not sure how to respond to that.")()
    print(response)
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()
    if intent == "end":
        exit()
