from flask import Flask
import os

from .db import init_db, seed_plants, close_db
from .weather_theme import get_theme_settings_and_weather, build_theme_class


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "tend-dev-key")

    with app.app_context():
        init_db()
        seed_plants()

    app.teardown_appcontext(close_db)

    @app.context_processor
    def inject_theme():
        settings, weather = get_theme_settings_and_weather()
        theme_class = build_theme_class(settings, weather)
        return dict(theme_class=theme_class)

    from .routes import bp
    app.register_blueprint(bp)

    return app


app = create_app()