import requests
from datetime import datetime


def format_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y")


def zip_to_latlon(zip_code):
    url = f"https://nominatim.openstreetmap.org/search?postalcode={zip_code}&country=US&format=json"
    response = requests.get(url, headers={"User-Agent": "tend-app"})
    results = response.json()
    if results:
        return float(results[0]["lat"]), float(results[0]["lon"])
    return None, None


def get_weather_conditions(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=precipitation&forecast_days=2"
    response = requests.get(url)
    data = response.json()
    hourly_precip = data["hourly"]["precipitation"]
    rain_expected = any(p > 0 for p in hourly_precip)
    if rain_expected:
        return {
            "message": "Rain expected within 48 hours. Good opportunity for planting or transplanting.",
            "mood": "rainy"
        }
    else:
        return {
            "message": "No rain expected soon. Consider watering after planting if soil is dry.",
            "mood": "sunny"
        }