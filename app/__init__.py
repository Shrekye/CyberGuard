import os
from flask import Flask, session
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
        "dev-secret-change-this-in-production-please"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

    # ======================
    # INIT EXTENSIONS
    # ======================
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
    oauth.init_app(app)

    # ======================
    # GOOGLE OAUTH
    # ======================
    google = oauth.register(
        name='google',
        client_id=os.environ.get("GOOGLE_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

    # ======================
    # CSP POLICY (déjà bien configurée)
    # ======================
    csp = {
        "default-src": ["'self'"],
        "script-src": ["'self'", "https://accounts.google.com"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:"],
        "frame-ancestors": ["'none'"],
        "object-src": ["'none'"]
    }
    
    Talisman(
        app, 
        content_security_policy=csp, 
        force_https=False,
        session_cookie_secure=False,
        session_cookie_http_only=True,
        strict_transport_security=False
    )

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
        return User.query.get(int(user_id))

    return app