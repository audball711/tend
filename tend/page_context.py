from .db import get_db, update_zone
from .helpers import format_date, get_weather_conditions, get_town_name

# -- BUILD ZONE DETAIL PAGE -- 

def build_zone_detail_context(zone_id):
    db = get_db()

    zone = db.execute(
        "SELECT * FROM zones WHERE id = ?",
        (zone_id,)
    ).fetchone()

    if zone is None:
        db.close()
        return None

    plants = db.execute(
        "SELECT id, common_name FROM plants ORDER BY common_name"
    ).fetchall()

    zone_plants = db.execute(
        """
        SELECT zone_plants.id, plants.common_name, plants.plant_type, zone_plants.quantity
        FROM zone_plants
        JOIN plants ON zone_plants.plant_id = plants.id
        WHERE zone_plants.zone_id = ?
        ORDER BY plants.common_name
        """,
        (zone_id,)
    ).fetchall()

    observations = db.execute(
        """
        SELECT id, note, created_at
        FROM observations
        WHERE zone_id = ?
        ORDER BY created_at DESC
        """,
        (zone_id,)
    ).fetchall()

    formatted_observations = [
        {
            "id": obs["id"],
            "note": obs["note"],
            "created_at": format_date(obs["created_at"])
        }
        for obs in observations
    ]

    settings = db.execute(
        "SELECT * FROM settings WHERE id = 1"
    ).fetchone()

    if settings and settings["latitude"] and settings["longitude"]:
        weather_conditions = get_weather_conditions(
            settings["latitude"],
            settings["longitude"]
        )
    else:
        weather_conditions = {
            "message": "Visit Settings to set your garden ZIP for weather forecasts.",
            "mood": "neutral"
        }

    db.close()

    weather_for_ai = (
        weather_conditions
        if isinstance(weather_conditions, dict) and "temp_high" in weather_conditions
        else None
    )

    return {
        "zone": zone,
        "plants": plants,
        "zone_plants": zone_plants,
        "observations": formatted_observations,
        "weather_conditions": weather_conditions,
        "weather_for_ai": weather_for_ai,
    }


# -- BUILD HOME PAGE -- 

def build_home_context():
    db = get_db()

    zones = db.execute(
        """
        SELECT
            zones.*,
            (
                SELECT COUNT(*)
                FROM zone_plants
                WHERE zone_plants.zone_id = zones.id
            ) AS plant_count,
            (
                SELECT note
                FROM observations
                WHERE observations.zone_id = zones.id
                ORDER BY created_at DESC
                LIMIT 1
            ) AS latest_note,
            (
                SELECT created_at
                FROM observations
                WHERE observations.zone_id = zones.id
                ORDER BY created_at DESC
                LIMIT 1
            ) AS latest_note_date
        FROM zones
        ORDER BY id DESC
        """
    ).fetchall()

    formatted_zones = [
        {
            "id": z["id"],
            "name": z["name"],
            "site_location": z["site_location"],
            "sun": z["sun"],
            "created_at": z["created_at"],
            "plant_count": z["plant_count"],
            "latest_note": z["latest_note"],
            "latest_note_date": format_date(z["latest_note_date"]) if z["latest_note_date"] else None
        }
        for z in zones
    ]

    settings = db.execute(
        "SELECT * FROM settings WHERE id = 1"
    ).fetchone()

    weather = None
    town_name = None

    if settings and settings["latitude"] and settings["longitude"]:
        weather = get_weather_conditions(
            settings["latitude"],
            settings["longitude"]
        )
        town_name = get_town_name(
            settings["latitude"],
            settings["longitude"]
        )

    db.close()

    return {
        "zones": formatted_zones,
        "weather": weather,
        "town_name": town_name
    }

# -- ZONE UPDATE FORM -- 

def update_zone_from_form(zone_id, form):
    name = form.get("name", "").strip()
    site_location = form.get("site_location", "").strip() or None
    sun = form.get("sun") or None

    if not name:
        return "Zone name is required."

    update_zone(zone_id, name, site_location, sun)
    return None