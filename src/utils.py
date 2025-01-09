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


def send_request(url):
    headers = {
        "User-Agent": "VoiceAssistant/1.0"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for HTTP status codes >= 400
    return response.json()


def get_lat_lon(geographical_name):
    base_url = f"https://nominatim.openstreetmap.org/search?q={geographical_name}&format=json&limit=1"

    try:
        # Fetch metadata for coordinates of location
        data = send_request(base_url)
        return {"lat": data[0]["lat"], "lon": data[0]["lon"]}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except KeyError as e:
        return {"error": f"Unexpected response structure: {e}"}


def get_forecast(geographical_name):
    # Get lat and lon
    coordinates = get_lat_lon(geographical_name)
    if "error" in coordinates:
        return {"error": coordinates["error"]}

    base_url = f"https://api.weather.gov/points/{coordinates["lat"]},{coordinates["lon"]}"

    try:
        # Fetch metadata for the location
        data = send_request(base_url)

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

