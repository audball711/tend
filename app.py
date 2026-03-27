from flask import Flask, redirect, render_template, request, flash
import sqlite3
from helpers import get_weather_conditions, zip_to_latlon, format_date, get_ai_suggestions, get_town_name
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "tend-dev-key")


def get_db():
    # create folder if it doesnt exist
    os.makedirs("instance", exist_ok=True)
    conn = sqlite3.connect("instance/tend.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    with open("schema.sql") as f:
        db.executescript(f.read())
    db.commit()

def seed_plants():
    db = get_db()

    # check if plants already exist
    count = db.execute("SELECT COUNT(*) as count FROM plants").fetchone()

    if count["count"] == 0:
        with open("plants.sql") as f:
            db.executescript(f.read())
        db.commit()

init_db()
seed_plants()

# weather theme in settings 
@app.context_processor
def inject_theme():
    db = get_db()

    settings = db.execute(
        "SELECT * FROM settings WHERE id = 1"
    ).fetchone()

    weather = None
    theme_mode = "weather"
    theme_class = "neutral day"

    if settings:
        try:
            theme_mode = settings["theme_mode"] or "weather"
        except (KeyError, IndexError):
            theme_mode = "weather"

        if settings["latitude"] and settings["longitude"]:
            weather = get_weather_conditions(
                settings["latitude"],
                settings["longitude"]
            )

    hour = datetime.now().hour

    if 6 <= hour < 9:
        time_class = "dawn"
    elif 9 <= hour < 17:
        time_class = "day"
    elif 17 <= hour < 20:
        time_class = "dusk"
    else:
        time_class = "night"

    if theme_mode == "base":
        theme_class = f"base-theme {time_class}"
    elif theme_mode in ["sunny", "rainy", "cloudy", "neutral"]:
        theme_class = f"{theme_mode} {time_class}"
    else:
        if weather and weather.get("mood"):
            theme_class = f"{weather['mood']} {time_class}"
        else:
            theme_class = f"neutral {time_class}"

    db.close()
    return dict(theme_class=theme_class)



@app.route("/")
def home():
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

    formatted_zones = []

    for z in zones:
        formatted_zones.append({
            "id": z["id"],
            "name": z["name"],
            "site_location": z["site_location"],
            "sun": z["sun"],
            "created_at": z["created_at"],
            "plant_count": z["plant_count"],
            "latest_note": z["latest_note"],
            "latest_note_date": format_date(z["latest_note_date"]) if z["latest_note_date"] else None
        })

    settings = db.execute("SELECT * FROM settings WHERE id = 1").fetchone()

    weather = None
    if settings and settings["latitude"] and settings["longitude"]:
        weather = get_weather_conditions(settings["latitude"], settings["longitude"])

    settings = db.execute("SELECT * FROM settings WHERE id = 1").fetchone()

    town_name = None

    if settings and settings["latitude"] and settings["longitude"]:
        town_name = get_town_name(
            settings["latitude"],
            settings["longitude"]
    )

    db.close()

    return render_template(
        "home.html",
        zones=formatted_zones,
        weather=weather,
        town_name=town_name
    )


@app.route("/zones/new", methods=["GET", "POST"])
def zones_new():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        site_location = request.form.get("site_location", "").strip() or None
        sun = request.form.get("sun") or None
        forecast_zip = request.form.get("forecast_zip", "").strip() or None

        # validate
        errors = []
        if not name:
            errors.append("Zone name is required.")
        if forecast_zip and (not forecast_zip.isdigit() or len(forecast_zip) != 5):
            errors.append("ZIP code must be exactly 5 digits.")

        if errors:
            for error in errors:
                flash(error)
            return redirect("/zones/new")
           

        latitude, longitude = None, None
        if forecast_zip:
            latitude, longitude = zip_to_latlon(forecast_zip)

        db = get_db()
        db.execute(
            "INSERT INTO zones (name, site_location, sun) VALUES (?, ?, ?)",
            (name, site_location, sun)
        )
        db.commit()
        db.close()

        return redirect("/")

    return render_template("zones_new.html")

@app.route("/zones/<int:zone_id>")
def zone_detail(zone_id):
    db = get_db()

    zone = db.execute(
        "SELECT * FROM zones WHERE id = ?",
        (zone_id,)
    ).fetchone()

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

    formatted_observations = []

    for obs in observations:
        formatted_observations.append({
            "id": obs["id"],
            "note": obs["note"],
            "created_at": format_date(obs["created_at"])
        })

        #revisit - do we need this 

    suggested_plants = []

    if zone["sun"]:
        suggested_plants = db.execute(
            """
            SELECT id, common_name, plant_type, sun
            FROM plants
            WHERE sun = ?
            AND id NOT IN (
                SELECT plant_id FROM zone_plants WHERE zone_id = ?
            )
            ORDER BY plant_type, common_name
            """,
            (zone["sun"], zone_id)
        ).fetchall()

    settings = db.execute("SELECT * FROM settings WHERE id = 1").fetchone()

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

    ai_suggestions = None

    return render_template(
        "zone_detail.html",
        zone=zone,
        plants=plants,
        zone_plants=zone_plants,
        observations=formatted_observations,
        suggested_plants=suggested_plants,
        weather_conditions=weather_conditions,
        ai_suggestions=ai_suggestions
    )


@app.route("/zones/<int:zone_id>/suggestion", methods=["POST"])
def zone_detail_suggestion(zone_id):
    db = get_db()

    zone = db.execute(
        "SELECT * FROM zones WHERE id = ?",
        (zone_id,)
    ).fetchone()

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

    formatted_observations = []

    for obs in observations:
        formatted_observations.append({
            "id": obs["id"],
            "note": obs["note"],
            "created_at": format_date(obs["created_at"])
        })

    suggested_plants = []

    if zone["sun"]:
        suggested_plants = db.execute(
            """
            SELECT id, common_name, plant_type, sun
            FROM plants
            WHERE sun = ?
            AND id NOT IN (
                SELECT plant_id FROM zone_plants WHERE zone_id = ?
            )
            ORDER BY plant_type, common_name
            """,
            (zone["sun"], zone_id)
        ).fetchall()

    settings = db.execute("SELECT * FROM settings WHERE id = 1").fetchone()

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

    ai_suggestions = get_ai_suggestions(
        zone["name"],
        zone["sun"],
        zone_plants,
        formatted_observations,
        suggested_plants,
        weather_conditions if isinstance(weather_conditions, dict) and "temp_high" in weather_conditions else None
    )

    return render_template(
        "zone_detail.html",
        zone=zone,
        plants=plants,
        zone_plants=zone_plants,
        observations=formatted_observations,
        suggested_plants=suggested_plants,
        weather_conditions=weather_conditions,
        ai_suggestions=ai_suggestions
    )

@app.route("/zones/<int:zone_id>/add-plant", methods=["POST"])
def add_plant_to_zone(zone_id):
    plant_id = request.form.get("plant_id")
    quantity = request.form.get("quantity", "1").strip()

    if not plant_id:
        flash("Please select a plant.")
        return redirect(f"/zones/{zone_id}")

    if not quantity.isdigit() or int(quantity) < 1:
        quantity = 1

    db = get_db()
    db.execute(
        "INSERT INTO zone_plants (zone_id, plant_id, quantity) VALUES (?, ?, ?)",
        (zone_id, plant_id, int(quantity))
    )
    db.commit()
    db.close()

    return redirect(f"/zones/{zone_id}")

@app.route("/zone-plants/<int:id>/delete", methods=["POST"])
def delete_zone_plant(id):

    db = get_db()

    # get zone id for redirecting

    row = db.execute(
        "SELECT zone_id FROM zone_plants WHERE id = ?",
        (id,)
    ).fetchone()

    db.execute(
        "DELETE FROM zone_plants WHERE id = ?",
        (id,)
    )

    db.commit()
    db.close()

    return redirect(f"/zones/{row['zone_id']}")

@app.route("/zones/<int:zone_id>/add-observation", methods=["POST"])
def add_observation(zone_id):
    note = request.form.get("note", "").strip()

    if note:
        db = get_db()
        db.execute(
            "INSERT INTO observations (zone_id, note) VALUES (?, ?)",
            (zone_id, note)
        )
        db.commit()
        db.close()

    return redirect(f"/zones/{zone_id}")


@app.route("/settings", methods=["GET", "POST"])
def settings():
    db = get_db()

    if request.method == "POST":
        home_zip = request.form.get("home_zip", "").strip() or None
        theme_mode = request.form.get("theme_mode") or "weather"

        if home_zip and (not home_zip.isdigit() or len(home_zip) != 5):
            flash("ZIP code must be exactly 5 digits.")
            db.close()
            return redirect("/settings")

        latitude, longitude = None, None
        town_name = None

        if home_zip:
            latitude, longitude = zip_to_latlon(home_zip)

            if latitude is None:
                flash("ZIP code not found. Please try another.")
                db.close()
                return redirect("/settings")

            town_name = get_town_name(latitude, longitude)

        db.execute(
            """
            UPDATE settings
            SET home_zip = ?, latitude = ?, longitude = ?, theme_mode = ?, town_name = ?
            WHERE id = 1
            """,
            (home_zip, latitude, longitude, theme_mode, town_name)
        )
        db.commit()
        db.close()
        return redirect("/settings")

    current = db.execute("SELECT * FROM settings WHERE id = 1").fetchone()
    db.close()

    town_name = current["town_name"] if current else None

    return render_template("settings.html", settings=current, town_name=town_name)

@app.route("/zones/<int:zone_id>/edit", methods=["GET", "POST"])
def zone_edit(zone_id):
    db = get_db()
    zone = db.execute("SELECT * FROM zones WHERE id = ?", (zone_id,)).fetchone()

    if not zone:
        flash("Zone not found.")
        db.close()
        return redirect("/")

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        site_location = request.form.get("site_location", "").strip() or None
        sun = request.form.get("sun") or None

        errors = []
        if not name:
            errors.append("Zone name is required.")

        if errors:
            for error in errors:
                flash(error)
            db.close()
            return redirect(f"/zones/{zone_id}/edit")

        db.execute(
            "UPDATE zones SET name = ?, site_location = ?, sun = ? WHERE id = ?",
            (name, site_location, sun, zone_id)
        )
        db.commit()
        db.close()
        return redirect(f"/zones/{zone_id}")

    db.close()
    return render_template("zone_edit.html", zone=zone)


@app.route("/zones/<int:zone_id>/delete", methods=["POST"])
def zone_delete(zone_id):
    db = get_db()

    # delete children first, then the zone
    db.execute("DELETE FROM observations WHERE zone_id = ?", (zone_id,))
    db.execute("DELETE FROM zone_plants WHERE zone_id = ?", (zone_id,))
    db.execute("DELETE FROM zones WHERE id = ?", (zone_id,))

    db.commit()
    db.close()

    flash("Garden space deleted.")
    return redirect("/")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
