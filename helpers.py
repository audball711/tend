import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()


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
    

def get_ai_suggestions(zone_name, sun, zone_plants, observations):
    # Don't call the API if there's nothing to analyze
    if not observations:
        return None

    # Build a readable list of current plants
    plant_list = ", ".join([p["common_name"] for p in zone_plants]) if zone_plants else "none yet"

    # Build a readable list of recent observations (last 5)
    observation_list = "\n".join([f"- {obs['note']}" for obs in observations[:10]])

    prompt = f"""You are a knowledgeable garden assistant. Based on the following garden zone information, provide 2-3 specific, actionable suggestions.

Zone: {zone_name}
Sun exposure: {sun}
Current plants: {plant_list}
Recent observations:
{observation_list}

Respond with 2-3 short, practical suggestions based on the observations. Each suggestion should be 1-2 sentences. Be specific to what was observed. Do not use bullet points or numbering — just separate suggestions with a blank line."""

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text