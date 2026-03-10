import requests
import os
import anthropic
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


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
            return float(results[0]["lat"]), float(results[0]["lon"])
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
            message = "Rain expected within 24 hours. Good opportunity for planting or transplanting."
        elif avg_cloud > 60:
            mood = "cloudy"
            message = "Cloudy skies ahead. Good conditions for garden work and transplanting."
        else:
            mood = "sunny"
            message = "Clear skies expected. Great time to observe your garden."

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
            catalog_context = f"\nPlants available in the Tend catalog that match this zone's sun conditions: {catalog_names}\n"

        weather_context = ""
        if weather and weather.get("temp_high"):
            weather_context = f"""
Current weather conditions:
- Temperature: {weather['temp_low']}°F low, {weather['temp_high']}°F high
- Humidity: {weather['humidity']}%
- Wind: {weather['wind_mph']} mph
- Cloud cover: {weather['cloud_cover']}%
- UV index: {weather['uv_index']}
- Rain expected: {"yes" if weather['rain_expected'] else "no"}
"""

        prompt = f"""You are a knowledgeable garden assistant. Based on the following garden zone information, provide 2-3 specific, actionable suggestions.

Zone: {zone_name}
Sun exposure: {sun}
Current plants: {plant_list}
{catalog_context}
{weather_context}
Recent observations:
{observation_list}

Respond with 2-3 short, practical suggestions. Where relevant, recommend specific plants from the Tend catalog. Each suggestion should be 1-2 sentences. Be specific to what was observed. Do not use bullet points or numbering — just separate suggestions with a blank line."""

        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text

    except Exception as e:
        print(f"AI suggestions failed: {e}")
        return None