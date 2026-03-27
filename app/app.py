# -- IMPORTS -- 

from flask import Flask, redirect, render_template, request, flash
from app.helpers import get_ai_suggestions
from app.db import get_db, init_db, seed_plants, get_zone_or_none, get_settings
from app.page_context import build_zone_detail_context, build_home_context, update_zone_from_form
from app.weather_theme import get_theme_settings_and_weather, build_theme_class
import os

# -- APP SETUP -- 

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "tend-dev-key")

# -- DB STRUCTURE AND PLANT DATA -- 

init_db()
seed_plants()

#  -- CONTEXT PROCESSOR --

@app.context_processor
def inject_theme():
    settings, weather = get_theme_settings_and_weather()
    theme_class = build_theme_class(settings, weather)
    return dict(theme_class=theme_class)


# -- ROUTE FOR HOME PAGE AND NEW ZONE -- 

@app.route("/")
def home():
    context = build_home_context()
    return render_template("home.html", **context)

@app.route("/zones/new", methods=["GET", "POST"])
def zones_new():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        site_location = request.form.get("site_location", "").strip() or None
        sun = request.form.get("sun") or None

        if not name:
            flash("Zone name is required.")
            return redirect("/zones/new")

        db = get_db()
        db.execute(
            "INSERT INTO zones (name, site_location, sun) VALUES (?, ?, ?)",
            (name, site_location, sun)
        )
        db.commit()
        db.close()

        return redirect("/")

    return render_template("zones_new.html")

# -- ROUTE FOR ZONE DETAIL -- 


@app.route("/zones/<int:zone_id>")
def zone_detail(zone_id):
    context = build_zone_detail_context(zone_id)

    if context is None:
        flash("That garden space could not be found.")
        return redirect("/")

    show_insight = request.args.get("insight") == "1"
   
    ai_suggestions = None

    if show_insight:
        ai_suggestions = get_ai_suggestions(
            context["zone"]["name"],
            context["zone"]["sun"],
            context["zone_plants"],
            context["observations"],
            context["weather_for_ai"]
        )

    context["ai_suggestions"] = ai_suggestions

    context.pop("weather_for_ai", None)

    return render_template("zone_detail.html", **context)

# -- ROUTES FOR ZONE ACTIONS -- 

@app.route("/zones/<int:zone_id>/add-plant", methods=["POST"])
def add_plant_to_zone(zone_id):

    zone = get_zone_or_none(zone_id)
    if zone is None:
        flash("That garden space could not be found.")
        return redirect("/")

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

    if row is None:
        db.close()
        flash("That plant entry could not be found.")
        return redirect("/")

    db.execute(
        "DELETE FROM zone_plants WHERE id = ?",
        (id,)
    )

    db.commit()
    db.close()

    return redirect(f"/zones/{row['zone_id']}")

@app.route("/zones/<int:zone_id>/add-observation", methods=["POST"])
def add_observation(zone_id):
    zone = get_zone_or_none(zone_id)
    if zone is None:
        flash("That garden space could not be found.")
        return redirect("/")


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

# -- ROUTE FOR SETTINGS -- 

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        error = update_settings_from_form(request.form)
        if error:
            flash(error)
        return redirect("/settings")

    current = get_settings()
    town_name = current["town_name"] if current else None

    return render_template("settings.html", settings=current, town_name=town_name)

# -- ROUTES FOR ZONE EDITING -- 

@app.route("/zones/<int:zone_id>/edit", methods=["GET", "POST"])
def zone_edit(zone_id):
    zone = get_zone_or_none(zone_id)

    if zone is None:
        flash("That garden space could not be found.")
        return redirect("/")

    if request.method == "POST":
        error = update_zone_from_form(zone_id, request.form)
        if error:
            flash(error)
            return redirect(f"/zones/{zone_id}/edit")

        return redirect(f"/zones/{zone_id}")

    return render_template("zone_edit.html", zone=zone)

@app.route("/zones/<int:zone_id>/delete", methods=["POST"])
def zone_delete(zone_id):
    db = get_db()

    zone = db.execute(
        "SELECT * FROM zones WHERE id = ?",
        (zone_id,)
    ).fetchone()

    if zone is None:
        db.close()
        flash("That garden space could not be found.")
        return redirect("/")

    # delete children first, then the zone
    db.execute("DELETE FROM observations WHERE zone_id = ?", (zone_id,))
    db.execute("DELETE FROM zone_plants WHERE zone_id = ?", (zone_id,))
    db.execute("DELETE FROM zones WHERE id = ?", (zone_id,))

    db.commit()
    db.close()

    flash("Garden space deleted.")
    return redirect("/")