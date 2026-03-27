import os
import sqlite3


def get_db():
    os.makedirs("instance", exist_ok=True)
    conn = sqlite3.connect("instance/tend.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()
    with open("schema.sql") as f:
        db.executescript(f.read())
    db.commit()
    db.close()


def seed_plants():
    db = get_db()
    count = db.execute("SELECT COUNT(*) as count FROM plants").fetchone()

    if count["count"] == 0:
        with open("plants.sql") as f:
            db.executescript(f.read())
        db.commit()

    db.close()


def get_zone_or_none(zone_id):
    db = get_db()
    zone = db.execute(
        "SELECT * FROM zones WHERE id = ?",
        (zone_id,)
    ).fetchone()
    db.close()
    return zone


# settings 

def get_settings():
    db = get_db()
    current = db.execute("SELECT * FROM settings WHERE id = 1").fetchone()
    db.close()
    return current


def save_settings(home_zip, latitude, longitude, theme_mode, town_name):
    db = get_db()
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

    # -- update zone -- 

def update_zone(zone_id, name, site_location, sun): 
    db = get_db()
    db.execute(
        "UPDATE zones SET name = ?, site_location = ?, sun = ? WHERE id = ?",
        (name, site_location, sun, zone_id)
        )
    db.commit()
    db.close()