import requests
import os
import anthropic
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def build_weather_message(mood, temp_high=None, humidity=None, wind_mph=None):
    if mood == "rainy":
        return "Rain arriving or damp conditions — watering is probably unnecessary today."

    if mood == "sunny":
        if temp_high is not None and temp_high >= 80:
            return "Warm bright weather — check soil sooner, especially in sunnier spots."
        return "Bright conditions today — a good day to check moisture before watering."

    if mood == "cloudy":
        if humidity is not None and humidity >= 75:
            return "Cool cloudy air may slow drying — hold off watering until you check the soil."
        return "Gentle cloudy weather — most beds may dry a little more slowly today."

    return "Calm garden weather — check the soil first and water only if needed."


def format_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y")
    except Exception:
        return date_string


def zip_to_latlon(zip_code):
    try:
        url = f"https://nominatim.openstreetmap.org/search?postalcode={zip_code}&country=US&format=json"
        response = requests.get(url, headers={"User-Agent": "tend-app"}, timeout=5)
        results = response.json()
        if results:
            return float(results[0]["lat"]), float(results[0]["lon"]),
        return None, None
    except Exception as e:
        print(f"ZIP lookup failed: {e}")
        return None, None


def get_weather_conditions(latitude, longitude):
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            f"&hourly=precipitation,cloudcover,relativehumidity_2m,windspeed_10m,uv_index"
            f"&daily=temperature_2m_max,temperature_2m_min"
            f"&temperature_unit=fahrenheit"
            f"&windspeed_unit=mph"
            f"&forecast_days=2"
        )

        response = requests.get(url, timeout=5)
        data = response.json()

        hourly_precip = data["hourly"]["precipitation"]
        hourly_clouds = data["hourly"]["cloudcover"]
        hourly_humidity = data["hourly"]["relativehumidity_2m"]
        hourly_wind = data["hourly"]["windspeed_10m"]
        hourly_uv = data["hourly"]["uv_index"]
        daily_max = data["daily"]["temperature_2m_max"]
        daily_min = data["daily"]["temperature_2m_min"]

        rain_expected = any(p > 0 for p in hourly_precip[:24])
        avg_cloud = sum(hourly_clouds[:24]) / 24
        avg_humidity = sum(hourly_humidity[:24]) / 24
        avg_wind = sum(hourly_wind[:24]) / 24
        max_uv = max(hourly_uv[:24])
        temp_high = daily_max[0]
        temp_low = daily_min[0]

        if rain_expected:
            mood = "rainy"
        elif avg_cloud > 60:
            mood = "cloudy"
        else:
            mood = "sunny"

        message = build_weather_message(
            mood,
            temp_high=round(temp_high),
            humidity=round(avg_humidity),
            wind_mph=round(avg_wind)
        )

        return {
            "mood": mood,
            "message": message,
            "temp_high": round(temp_high),
            "temp_low": round(temp_low),
            "humidity": round(avg_humidity),
            "wind_mph": round(avg_wind),
            "cloud_cover": round(avg_cloud),
            "uv_index": round(max_uv),
            "rain_expected": rain_expected
        }

    except Exception as e:
        print(f"Weather fetch failed: {e}")
        return {
            "mood": "neutral",
            "message": "Weather unavailable right now.",
            "temp_high": None,
            "temp_low": None,
            "humidity": None,
            "wind_mph": None,
            "cloud_cover": None,
            "uv_index": None,
            "rain_expected": False
        }


def get_ai_suggestions(zone_name, sun, zone_plants, observations, catalog_plants=None, weather=None):
    try:
        if not observations:
            return None

        plant_list = ", ".join([p["common_name"] for p in zone_plants]) if zone_plants else "none yet"
        observation_list = "\n".join([f"- {obs['note']}" for obs in observations[:10]])

        catalog_context = ""
        if catalog_plants:
            catalog_names = ", ".join([p["common_name"] for p in catalog_plants])
            catalog_context = (
                f"Plants available in the Tend catalog that match this zone's sun conditions: "
                f"{catalog_names}"
            )

        weather_context = ""
        if weather and weather.get("temp_high"):
            weather_context = f"""Current weather conditions:
- Temperature: {weather['temp_low']}°F low, {weather['temp_high']}°F high
- Humidity: {weather['humidity']}%
- Wind: {weather['wind_mph']} mph
- Cloud cover: {weather['cloud_cover']}%
- UV index: {weather['uv_index']}
- Rain expected: {"yes" if weather['rain_expected'] else "no"}"""

        prompt = f"""
ROLE
You are Tend, a calm and thoughtful garden companion.

TASK
Write ONE very short Tend Note about this garden zone.

RULES
- maximum 14 words
- exactly 1 sentence
- calm, observant, and natural
- no lists
- no extra explanation
- no quotation marks
- no commands

CONTEXT
Zone name: {zone_name}
Sun exposure: {sun}
Plants growing here: {plant_list}

{catalog_context}

{weather_context}

Recent observations:
{observation_list}

OUTPUT
Return only the Tend Note sentence.
"""

        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=30,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text.strip()

    except Exception as e:
        print(f"AI suggestions failed: {e}")
        return None
    

def zip_to_town(zip_code):
    try:
        url = f"https://nominatim.openstreetmap.org/search?postalcode={zip_code}&country=US&format=json"
        response = requests.get(url, headers={"User-Agent": "tend-app"}, timeout=5)
        results = response.json()

        if results:
            address = results[0].get("display_name", "")
            parts = [part.strip() for part in address.split(",") if part.strip()]
            if parts:
                return parts[0]

        return None
    except Exception as e:
        print(f"Town lookup failed: {e}")
        return None