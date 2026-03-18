import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth()
google = None

def create_app():
    global google
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config["SECRET_KEY"] = "cyberforum-secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- INTEGRATION GOOGLE ---
    oauth.init_app(app)
    google = oauth.register(
        name='google',
        client_id=os.environ.get("GOOGLE_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    from .models import User  # <-- important pour le user_loader
    from .routes import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    # Flask-Login : dire comment charger un utilisateur
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app