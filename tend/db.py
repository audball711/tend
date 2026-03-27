import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from flask import g

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BASE_DIR / "schema.sql"
PLANTS_PATH = BASE_DIR / "plants.sql"


def get_db():
    if "db" not in g:
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            raise RuntimeError("DATABASE_URL is not set.")

        g.db = psycopg.connect(
            database_url,
            row_factory=dict_row,
        )
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with db.cursor() as cur:
        cur.execute(schema_sql)

    db.commit()


def seed_plants():
    db = get_db()

    with db.cursor() as cur:
        cur.execute("SELECT COUNT(*) AS count FROM plants")
        count = cur.fetchone()

        if count["count"] == 0:
            with open(PLANTS_PATH, "r", encoding="utf-8") as f:
                plants_sql = f.read()
            cur.execute(plants_sql)

    db.commit()


def get_zone_or_none(zone_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "SELECT * FROM zones WHERE id = %s",
            (zone_id,)
        )
        return cur.fetchone()


def get_settings():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM settings WHERE id = 1")
        return cur.fetchone()


def save_settings(home_zip, latitude, longitude, theme_mode, town_name):
    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            """
            UPDATE settings
            SET home_zip = %s, latitude = %s, longitude = %s, theme_mode = %s, town_name = %s
            WHERE id = 1
            """,
            (home_zip, latitude, longitude, theme_mode, town_name)
        )
    db.commit()


def update_zone(zone_id, name, site_location, sun):
    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "UPDATE zones SET name = %s, site_location = %s, sun = %s WHERE id = %s",
            (name, site_location, sun, zone_id)
        )
    db.commit()