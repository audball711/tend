from flask import Flask, redirect, render_template, request
import sqlite3
from helpers import get_weather_conditions, zip_to_latlon, format_date


app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("instance/tend.db")
    conn.row_factory = sqlite3.Row
    return conn

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
            )AS latest_note_date
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

    db.close()

    return render_template("home.html", zones=formatted_zones, weather=weather)

@app.route("/zones/new", methods=["GET","POST"])
def zones_new():
    if request.method == "POST":
        name = request.form.get("name")
        site_location = request.form.get("site_location")
        sun = request.form.get("sun") or None

        db = get_db()
        db.execute("INSERT INTO zones (name, site_location, sun) VALUES (?, ?, ?)", 
                   (name, site_location, sun))
        
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

    #date and time readability 

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
        weather_conditions = get_weather_conditions(settings["latitude"], settings["longitude"])
    else:
        weather_conditions = {"message": "Visit Settings to set your garden ZIP for weather forecasts.", "mood": "neutral"}

    db.close()

    return render_template("zone_detail.html", 
                           zone=zone, 
                           plants=plants,
                           zone_plants=zone_plants,
                           observations=formatted_observations,
                           suggested_plants=suggested_plants,
                           weather_conditions=weather_conditions)

@app.route("/zones/<int:zone_id>/add-plant", methods=["POST"])
def add_plant_to_zone(zone_id):
    plant_id = request.form.get("plant_id")
    quantity = request.form.get("quantity") or 1

    db = get_db()
    db.execute(
        "INSERT INTO zone_plants (zone_id, plant_id, quantity) VALUES (?, ?, ?)",
        (zone_id, plant_id, quantity)
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

        latitude, longitude = None, None
        if home_zip:
            latitude, longitude = zip_to_latlon(home_zip)

        db.execute(
            "UPDATE settings SET home_zip = ?, latitude = ?, longitude = ? WHERE id = 1",
            (home_zip, latitude, longitude)
        )
        db.commit()
        db.close()
        return redirect("/settings")

    current = db.execute("SELECT * FROM settings WHERE id = 1").fetchone()
    db.close()

    return render_template("settings.html", settings=current)




if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
