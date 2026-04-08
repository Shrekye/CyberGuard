import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_talisman import Talisman
from authlib.integrations.flask_client import OAuth
from datetime import timedelta

# ======================
# EXTENSIONS
# ======================
db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth()
google = None  # sera défini dans create_app


def create_app():
    global google

    # ======================
    # APP INIT
    # ======================
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "dev-secret-change-this-in-production"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ======================
    # SESSION SECURITY
    # ======================
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SECURE"] = False  # True en production (HTTPS)
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    app.config["REMEMBER_COOKIE_HTTPONLY"] = True
    app.config["REMEMBER_COOKIE_SECURE"] = False
    app.config["REMEMBER_COOKIE_SAMESITE"] = "Lax"

    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)

    # ======================
    # INIT EXTENSIONS
    # ======================
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
    login_manager.session_protection = "strong"

    oauth.init_app(app)

    # ======================
    # GOOGLE OAUTH
    # ======================
    google = oauth.register(
        name="google",
        client_id=os.environ.get("GOOGLE_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid email profile"
        }
    )

    # ======================
    # CSP POLICY
    # ======================
    csp = {
        "default-src": ["'self'"],

        # Google OAuth scripts
        "script-src": [
            "'self'",
            "https://accounts.google.com"
        ],

        # inline css souvent utilisé par templates
        "style-src": [
            "'self'",
            "'unsafe-inline'"
        ],

        # avatars google
        "img-src": [
            "'self'",
            "data:",
            "https://lh3.googleusercontent.com"
        ],

        # OAuth popup
        "frame-src": [
            "https://accounts.google.com"
        ],

        "frame-ancestors": ["'none'"],
        "object-src": ["'none'"]
    }

    Talisman(
        app,
        content_security_policy=csp,
        force_https=False,           # True en prod
        strict_transport_security=False
    )

    @app.after_request
    def disable_cache(response):
        response.headers["Cache-Control"] = "no-store"
        return response

    # ======================
    # BLUEPRINTS
    # ======================
    from .models import User
    from .routes import main_bp

    app.register_blueprint(main_bp)

    # ======================
    # CREATE DB TABLES
    # ======================
    with app.app_context():
        db.create_all()

    # ======================
    # USER LOADER
    # ======================
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app
