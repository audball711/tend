# Tend (Working Name)

#### Video Demo: https://youtu.be/urqQSYvYAzM

#### Live Application: https://tend-3b2l.onrender.com

---

## Demo Environment

The live application is currently running as a shared demo space. This means that all users interact with the same set of zones and observations rather than having separate accounts. This approach was chosen to keep the application simple for demonstration and testing purposes.

In future iterations, the application could be extended to support user accounts and personalized spaces, but for this version the shared environment allows multiple users to explore the full functionality of the system without requiring authentication.

---

## Overview

Tend is a web-based application designed to help users track, understand, and reflect on their garden or growing spaces. The goal of this project is to create a simple, yet intelligent, zone-based system that allows users to log observations about their environment and receive helpful insights without needing to manually analyze everything themselves.

The core idea behind Tend is that people may become overwhelmed with what is happening in their garden over time, especially new gardeners. Instead of relying on memory or complex tracking systems, Tend provides a calm and intuitive interface where users can organize their space into zones and record what they notice.

Over time, the system uses these observations along with environmental context to generate reflections that help users better understand patterns and changes.

---

## Core Features

The main feature of the application is the concept of "zones." A zone represents a physical area such as a garden bed or section of land.

Each zone contains:

* Observations (user-entered notes)
* Environmental context (sun, location)
* A historical record of activity over time

Observations are timestamped and stored in the database so that users can build a history of what is happening in each space.

---

## Reflection System

A key feature of the system is the reflection engine. When a user clicks the reflect button, the application gathers recent observations and generates a single, focused insight.

Rather than overwhelming the user with multiple suggestions, the system is intentionally designed to return one meaningful thought at a time. This keeps the experience simple and supportive.

During development, I initially explored adding automatic plant suggestions for each zone. However, I chose to remove this feature because it was not truly tied to the user’s data and risked becoming generic.

Instead, I focused on generating insights based on actual observations, time, and environmental context. This decision helped keep the system grounded and aligned with real conditions.

---

## Environmental Context & UI

Another important part of the project is the integration of location and weather context.

The application uses this information to influence both insights and the visual experience. The interface includes a theme system that adapts based on:

* Weather (sunny, rainy, cloudy, neutral)
* Time of day (dawn, day, dusk, night)

This creates a more immersive experience that reflects the user’s real environment.

---

## Architecture & Structure

The application is built using Flask as the backend framework and uses a PostgreSQL database to store zones, observations, settings, and related data.

During development, I refactored the database layer to fully support PostgreSQL, creating a more production-ready and consistent architecture.

### File Structure

* `tend/__init__.py`
  Uses the application factory pattern to create and configure the Flask app.

* `tend/routes.py`
  Contains all route logic, including rendering pages, handling forms, and triggering reflections.

* `tend/db.py`
  Manages database connections and queries using PostgreSQL.

* `tend/weather_theme.py`
  Handles weather-based theming and environmental context.

* `tend/page_context.py`
  Injects shared data (such as theme and weather) into templates.

* `tend/helpers.py`
  Contains utility functions used across the app.

* `templates/`
  Contains all HTML templates rendered using Jinja.

* `static/`
  Contains CSS and JavaScript assets, including dynamic theme styling.

* `schema.sql`
  Defines database structure.

* `plants.sql`
  Seeds initial plant data.

* `requirements.txt`
  Lists Python dependencies.

---

## Running the Application Locally

To run this application locally, a PostgreSQL database is required.

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a PostgreSQL database

Create a database and obtain a connection string.

### 3. Set environment variable

On macOS/Linux:

```bash
export DATABASE_URL="your_postgres_connection_string"
```

On Windows:

```bash
set DATABASE_URL=your_postgres_connection_string
```

### 4. Initialize database

The application will automatically:

* Create tables using `schema.sql`
* Seed plant data using `plants.sql` (if empty)

### 5. Run the app

```bash
flask run
```

---

## Important Notes

* This project uses **PostgreSQL**, not SQLite
* The app depends on the `DATABASE_URL` environment variable to run

---

## Design Philosophy

One of the key design decisions in this project was to prioritize simplicity.

Instead of building a complex system with many features, I focused on a small set of core interactions:

* Zones
* Observations
* Reflections

I also chose to present only one insight at a time to avoid overwhelming the user.

Another important decision was to treat the AI component as a supportive assistant rather than an authoritative system. The goal is to help users think more clearly and notice patterns, not to replace human judgment.

---

## Future Improvements

Future improvements could include:

* Plant-level tracking within zones
* A planning interface for garden layouts and materials
* A local-first version using a device such as a Raspberry Pi
* User accounts and personalized garden spaces

---

## Final Thoughts

Tend is designed to be a lightweight but thoughtful tool that helps users build awareness of their space over time.

By combining tracking, environmental context, and reflection, the application aims to create a calm and intuitive experience that supports both beginner and experienced gardeners.
