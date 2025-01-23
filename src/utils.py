import os
import pyttsx3
import time
from getpass import getpass
import requests
import feedparser
import qrcode
from PIL import Image
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL


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

        # Create the folder if it doesn't exist
        folder = "qr_codes"
        os.makedirs(folder, exist_ok=True)

        # Construct the full file path to save the image
        file_path = os.path.join(folder, filename)

        # Generate and save the QR code
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(file_path)
        return f"QR code saved as {filename} to {file_path}."
    except Exception as e:
        return f"An error occurred while generating the QR code: {e}"


def convert_image_format(file_path, extension):
    # Define valid image extensions
    valid_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")

    # Extract the current file extension
    _, current_extension = os.path.splitext(file_path)

    # Ensure extensions are case-insensitive
    current_extension = current_extension.lower()
    extension = extension.lower()

    # Check if the current file has a valid image extension
    if current_extension not in valid_extensions:
        return "The selected file is not a valid image file."

    # Check if the target extension is valid
    if extension not in valid_extensions:
        return f"The target extension is not a valid image format."

    try:
        # Open the image
        image = Image.open(file_path)

        # Check RGB <-> RGBA
        if current_extension in [".png", ".tiff"] and extension not in [".png", ".tiff", ".webp"]:
            # Convert the image to 'RGB' to discard the alpha channel for formats like JPEG
            image = image.convert("RGB")

        # Convert and save the image in a different format
        new_file_path = file_path.replace(current_extension, extension)
        image.save(new_file_path)

        return f"Image file was converted from {current_extension} to {extension} and saved as \n{new_file_path}"
    except Exception as e:
        return f"An error occurred during the conversion: {e}"


# This function adjusts the system volume, it is not application-based.
def adjust_volume(level=None):
    try:
        # Get the audio endpoint (default audio output device)
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(interface=IAudioEndpointVolume, clsctx=CLSCTX_ALL, pUnkOuter=None)
        volume = interface.QueryInterface(IAudioEndpointVolume)

        # Validate the level input and adjust volume
        if level is not None and 0 <= level <= 100:
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            return f"Volume successfully set to {int(level)}%"
        else:
            return "Error: Volume level must be between 0% and 100%"
    except Exception as e:
        return f"An error occurred while adjusting the volume: {e}"
