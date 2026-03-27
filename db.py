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