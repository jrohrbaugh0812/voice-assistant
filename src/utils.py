import pyttsx3
import time
from getpass import getpass
import requests
import feedparser
import qrcode


def text_to_speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Choose a different voice
    engine.setProperty('rate', 150)  # Adjust speech rate
    engine.setProperty('volume', 1.0)  # Adjust volume
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


def get_news():
    feed_url = "https://feeds.bbci.co.uk/news/rss.xml"  # Feed from BBC
    feed = feedparser.parse(feed_url)
    news_feed = ""
    for entry in feed.entries[:5]:  # Get the first five articles
        news_feed += f"Title: {entry.title}\nLink: {entry.link}\n"
    return news_feed


def get_joke():
    base_url = f"https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
    try:
        data = send_request(base_url)
        if data.get("error"):
            return {"error": data["error"]}
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except KeyError as e:
        return {"error": f"Unexpected response structure: {e}"}


def generate_qr_code(url, filename):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        return f"\nQR code save as {filename}."
    except Exception as e:
        return f"\nAn error occurred while generating the QR code: {e}"

