# -- IMPORTS -- 

from flask import redirect, render_template, request, flash, Blueprint

from .helpers import get_ai_suggestions
from .db import get_db, get_zone_or_none, get_settings
from .page_context import build_zone_detail_context, build_home_context, update_zone_from_form
from .weather_theme import update_settings_from_form

bp = Blueprint("main", __name__)

# -- ROUTE FOR HOME PAGE AND NEW ZONE -- 

@bp.route("/")
def home():
    context = build_home_context()
    return render_template("home.html", **context)

@bp.route("/zones/new", methods=["GET", "POST"])
def zones_new():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        site_location = request.form.get("site_location", "").strip() or None
        sun = request.form.get("sun") or None

        if not name:
            flash("Zone name is required.")
            return redirect("/zones/new")

        db = get_db()
        with db.cursor() as cur:
            cur.execute(
                "INSERT INTO zones (name, site_location, sun) VALUES (%s, %s, %s)",
                (name, site_location, sun)
            )
        db.commit()

        return redirect("/")

    return render_template("zones_new.html")

# -- ROUTE FOR ZONE DETAIL -- 


@bp.route("/zones/<int:zone_id>")
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

@bp.route("/zones/<int:zone_id>/add-plant", methods=["POST"])
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
    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO zone_plants (zone_id, plant_id, quantity) VALUES (%s, %s, %s)",
            (zone_id, plant_id, int(quantity))
        )
    db.commit()

    return redirect(f"/zones/{zone_id}")

@bp.route("/zone-plants/<int:id>/delete", methods=["POST"])
def delete_zone_plant(id):
    db = get_db()

    with db.cursor() as cur:
        cur.execute(
            "SELECT zone_id FROM zone_plants WHERE id = %s",
            (id,)
        )
        row = cur.fetchone()

        if row is None:
            flash("That plant entry could not be found.")
            return redirect("/")

        cur.execute(
            "DELETE FROM zone_plants WHERE id = %s",
            (id,)
        )

    db.commit()

    return redirect(f"/zones/{row['zone_id']}")

@bp.route("/zones/<int:zone_id>/add-observation", methods=["POST"])
def add_observation(zone_id):
    zone = get_zone_or_none(zone_id)
    if zone is None:
        flash("That garden space could not be found.")
        return redirect("/")

    note = request.form.get("note", "").strip()

    if note:
        db = get_db()
        with db.cursor() as cur:
            cur.execute(
                "INSERT INTO observations (zone_id, note) VALUES (%s, %s)",
                (zone_id, note)
            )
        db.commit()

    return redirect(f"/zones/{zone_id}")

# -- ROUTE FOR SETTINGS -- 

@bp.route("/settings", methods=["GET", "POST"])
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

@bp.route("/zones/<int:zone_id>/edit", methods=["GET", "POST"])
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

@bp.route("/zones/<int:zone_id>/delete", methods=["POST"])
def zone_delete(zone_id):
    db = get_db()

    with db.cursor() as cur:
        cur.execute(
            "SELECT * FROM zones WHERE id = %s",
            (zone_id,)
        )
        zone = cur.fetchone()

        if zone is None:
            flash("That garden space could not be found.")
            return redirect("/")

        cur.execute("DELETE FROM zones WHERE id = %s", (zone_id,))

    db.commit()

    flash("Garden space deleted.")
    return redirect("/")