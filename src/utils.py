import pyttsx3
import time
from getpass import getpass
import requests


def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_time():
    return time.strftime("%I:%M:%S %p", time.localtime())


def get_password():
    return getpass("What is your password? ")


def get_forecast(lat, lon):
    base_url = f"https://api.weather.gov/points/{lat},{lon}"

    try:
        # Fetch metadata for the location
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an error for HTTP status codes >= 400
        data = response.json()

        # Pull the forecast URL
        forecast_url = data["properties"]["forecast"]

        # Fetch forecast data
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        # Pull periods with temperature details
        return forecast_data["properties"]["periods"]
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except KeyError as e:
        return {"error": f"Unexpected response structure: {e}"}

