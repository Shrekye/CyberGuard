import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from authlib.integrations.flask_client import OAuth

# ======================
# EXTENSIONS
# ======================
db = SQLAlchemy()
login_manager = LoginManager()
#csrf = CSRFProtect()
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
        "dev-secret-change-this"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ======================
    # INIT EXTENSIONS
    # ======================
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    csrf.init_app(app)
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
    # CSP POLICY
    # ======================
    csp = {
        "default-src": ["'self'"],
        "script-src": ["'self'", "https://accounts.google.com"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:"],
        "frame-ancestors": ["'none'"],
        "object-src": ["'none'"]
    }
    Talisman(app, content_security_policy=csp, force_https=False)

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