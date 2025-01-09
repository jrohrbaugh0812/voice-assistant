import random
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
import webbrowser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from intents import get_intent
from recognizer import (recognize_save_note, recognize_email_body, recognize_email_subject)
from utils import (text_to_speech, get_time, get_password, get_forecast)


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
    print("You will have to answer the following questions by typing...")
    text_to_speech("You will have to answer the following questions by typing...")

    sender_email_address = input("What is your email address? ")
    password = get_password()
    receiver_email_address = input("What is the email address you want to contact? ")
    input_type = input("Do you want to type OR speak the subject and body contents? (type/speak): ").lower()
    if input_type == "type":
        email_subject = input("What would you like the subject of the email to be? ")
        email_body = input("What would you like the body of the email to be? ")
    elif input_type == "speak":
        email_subject = recognize_email_subject()
        email_body = recognize_email_body()
    else:
        return "Invalid input type"

    should_continue = input(f"Do you want to continue with this email? \n {sender_email_address} to "
                            f"{receiver_email_address} \n {email_subject} \n {email_body} \n\n y/n? ").lower()

    if should_continue != 'y':
        return "Discarded email"

    msg = MIMEMultipart()
    msg["From"] = sender_email_address
    msg["To"] = receiver_email_address
    msg["Subject"] = email_subject
    msg.attach(MIMEText(email_body, "plain"))

    # Sending the email (i.e., "msg")
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()  # Secure the connection
            server.login(sender_email_address, password)  # Login to the server
            server.sendmail(sender_email_address, receiver_email_address, msg.as_string())  # Send email
            return "Email sent successfully."
    except smtplib.SMTPAuthenticationError as auth_error:
        print(f"Authentication error: {auth_error.smtp_code} - {auth_error.smtp_error}")
        return "Authentication error. Check your email and password."
    except Exception as e:
        print(f"Full error: {e}")
        return f"An error occurred: {e}"


def get_weather():
    geographical_name = input("What is the name of the city, town, or county you want weather data from? ")

    data = get_forecast(geographical_name)

    if "error" in data:
        return f"Error: {data['error']}"
    else:
        # Format the forecast data for readability
        forecast = "\n".join(
            [f"{period['name']}: {period['temperature']}°{period['temperatureUnit']}, {period['shortForecast']}"
             for period in data]
        )
        return f"Here is the forecast for {geographical_name}:\n{forecast}"


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
    "weather": get_weather,
    "end": quit_program,
}


def respond(user_text):
    user_text = user_text.lower()
    intent = get_intent(user_text)
    response = COMMANDS.get(intent, lambda: "I'm not sure how to respond to that.")()
    print(response)
    text_to_speech(response)
    if intent == "end":
        exit()
