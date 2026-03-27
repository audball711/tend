from datetime import datetime

from .db import get_db, save_settings
from .helpers import get_weather_conditions, zip_to_latlon, get_town_name


def get_time_class():
    hour = datetime.now().hour

    if 6 <= hour < 9:
        return "dawn"
    if 9 <= hour < 17:
        return "day"
    if 17 <= hour < 20:
        return "dusk"
    return "night"


def get_theme_settings_and_weather():
    db = get_db()

    with db.cursor() as cur:
        cur.execute("SELECT * FROM settings WHERE id = 1")
        settings = cur.fetchone()

    weather = None
    if settings and settings["latitude"] and settings["longitude"]:
        weather = get_weather_conditions(
            settings["latitude"],
            settings["longitude"]
        )

    return settings, weather


def build_theme_class(settings, weather):
    theme_mode = settings["theme_mode"] if settings and settings["theme_mode"] else "weather"
    time_class = get_time_class()

    if theme_mode == "base":
        return f"base-theme {time_class}"

    if theme_mode in ["sunny", "rainy", "cloudy", "neutral"]:
        return f"{theme_mode} {time_class}"

    if weather and weather.get("mood"):
        return f"{weather['mood']} {time_class}"

    return f"neutral {time_class}"


def update_settings_from_form(form):
    home_zip = form.get("home_zip", "").strip() or None
    theme_mode = form.get("theme_mode") or "weather"

    if home_zip and (not home_zip.isdigit() or len(home_zip) != 5):
        return "ZIP code must be exactly 5 digits."

    latitude, longitude = None, None
    town_name = None

    if home_zip:
        latitude, longitude = zip_to_latlon(home_zip)

        if latitude is None:
            return "ZIP code not found. Please try another."

        town_name = get_town_name(latitude, longitude)

    save_settings(home_zip, latitude, longitude, theme_mode, town_name)
    return None