DROP TABLE IF EXISTS observations;
DROP TABLE IF EXISTS zone_plants;
DROP TABLE IF EXISTS plants;
DROP TABLE IF EXISTS zones;
DROP TABLE IF EXISTS settings;


CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY,
    home_zip TEXT,
    latitude REAL,
    longitude REAL,
    theme_mode TEXT DEFAULT 'weather'
    town_name TEXT
);

INSERT INTO settings (id, home_zip, latitude, longitude) VALUES (1, NULL, NULL, NULL);

CREATE TABLE IF NOT EXISTS zones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    site_location TEXT,
    sun TEXT CHECK (sun IN ('full', 'partial', 'shade')),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS plants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    common_name TEXT NOT NULL,
    latin_name TEXT,
    sun TEXT CHECK (sun IN ('full', 'partial', 'shade')),
    plant_type TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS zone_plants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_id INTEGER NOT NULL,
    plant_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (zone_id) REFERENCES zones(id),
    FOREIGN KEY (plant_id) REFERENCES plants(id)
);

CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_id INTEGER NOT NULL,
    note TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (zone_id) REFERENCES zones(id)
);


