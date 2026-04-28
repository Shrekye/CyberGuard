from flask import Blueprint, render_template, request, redirect, url_for, session, abort, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app.vault_client import get_secret
from .models import User, RedTopic, BlueTopic, PurpleTopic, Post
from . import db
from . import google
import secrets
import time
import random  # nosec
import re
import os
import uuid
import sys
import socket
import logging
import subprocess


main_bp = Blueprint("main", __name__)


# =========================
# LOGGER CONFIG
# =========================

logging.basicConfig(
    filename="app_info.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =========================
# CONFIG IMAGE
# =========================

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# =========================
# CSRF PROTECTION
# =========================

def generate_csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(32)
    return session["_csrf_token"]


def validate_csrf():
    token = session.get("_csrf_token")
    form_token = request.form.get("csrf_token")

    if not token or not form_token or token != form_token:
        abort(403, "CSRF token validation failed")


@main_bp.app_context_processor
def inject_csrf():
    return dict(csrf_token=generate_csrf_token())


# =========================
# VALIDATION HELPERS
# =========================

def validate_username(username):
    if not username or len(username) < 3 or len(username) > 50:
        return False
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', username))


def validate_password(password):
    if not password or len(password) < 8:
        return False
    return bool(re.search(r'[A-Za-z]', password) and re.search(r'[0-9]', password))


# =========================
# HOME
# =========================

@main_bp.route("/")
def index():
    red_topics = RedTopic.query.order_by(RedTopic.created_at.desc()).limit(10).all()
    blue_topics = BlueTopic.query.order_by(BlueTopic.created_at.desc()).limit(10).all()
    purple_topics = PurpleTopic.query.order_by(PurpleTopic.created_at.desc()).limit(10).all()

    return render_template(
        "index.html",
        red_topics=red_topics,
        blue_topics=blue_topics,
        purple_topics=purple_topics
    )


# =========================
# REGISTER
# =========================

@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        validate_csrf()

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not validate_username(username):
            return "Invalid username format", 400

        if not validate_password(password):
            return "Password must be at least 8 characters with letters and numbers", 400

        if User.query.filter_by(username=username).first():
            return "Username already exists!", 400

        time.sleep(0.5)

        user = User(
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("main.login"))

    return render_template("register.html")


# =========================
# LOGIN
# =========================

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        time.sleep(0.5)

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            session.permanent = True
            return redirect(url_for("main.index"))

        return "Invalid credentials", 401

    return render_template("login.html")


# =========================
# GOOGLE OAUTH
# =========================

@main_bp.route('/login/google')
def google_login():
    google.client_id = get_secret("cyberguard", "GOOGLE_CLIENT_ID")
    google.client_secret = get_secret("cyberguard", "GOOGLE_CLIENT_SECRET")
    redirect_uri = url_for('main.google_authorize', _external=True, _scheme="https")  # nosemgrep
    return google.authorize_redirect(redirect_uri)


@main_bp.route('/google/auth')
def google_authorize():
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')

        if user_info:
            email = user_info['email']
            user = User.query.filter_by(username=email).first()

            if not user:
                user = User(
                    username=email,
                    password=generate_password_hash(secrets.token_urlsafe(32))
                )
                db.session.add(user)
                db.session.commit()

            login_user(user, remember=True)
            session.permanent = True

    except Exception as e:
        return f"Authentication failed: {str(e)}", 401

    return redirect(url_for('main.index'))


# =========================
# LOGOUT
# =========================

@main_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


# =========================
# SECRET
# =========================

@main_bp.route("/secret")
def secret():
    return render_template("secret.html")


# =========================
# CREATE TOPIC (AVEC IMAGE)
# =========================

@main_bp.route("/create_topic", methods=["GET", "POST"])
@login_required
def create_topic():
    if request.method == "POST":
        validate_csrf()

        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category")

        image = request.files.get("image")
        image_filename = None

        if image and image.filename != "":
            if not allowed_file(image.filename):
                return "Invalid image format", 400

            filename = secure_filename(image.filename)
            unique_name = str(uuid.uuid4()) + "_" + filename

            upload_folder = current_app.config.get("UPLOAD_FOLDER", "static/uploads")
            os.makedirs(upload_folder, exist_ok=True)

            image_path = os.path.join(upload_folder, unique_name)
            image.save(image_path)

            image_filename = unique_name

        if not title or len(title) < 3 or len(title) > 200:
            return "Title must be between 3 and 200 characters", 400

        if len(content) > 10000:
            return "Content too long", 400

        if category not in ["red", "blue", "purple"]:
            return "Invalid category", 400

        time.sleep(0.3)

        if category == "red":
            topic = RedTopic(title=title, user_id=current_user.id)
        elif category == "blue":
            topic = BlueTopic(title=title, user_id=current_user.id)
        else:
            topic = PurpleTopic(title=title, user_id=current_user.id)

        db.session.add(topic)
        db.session.commit()

        if content or image_filename:
            post = Post(
                content=content,
                user_id=current_user.id,
                topic_id=topic.id,
                topic_type=category,
                image=image_filename
            )
            db.session.add(post)
            db.session.commit()

        return redirect(url_for("main.topic_view", category=category, topic_id=topic.id))

    return render_template("create_topic.html")


# =========================
# VIEW TOPIC
# =========================

@main_bp.route("/topic/<category>/<int:topic_id>", methods=["GET", "POST"])
@login_required
def topic_view(category, topic_id):
    if category == "red":
        topic = RedTopic.query.get_or_404(topic_id)
    elif category == "blue":
        topic = BlueTopic.query.get_or_404(topic_id)
    elif category == "purple":
        topic = PurpleTopic.query.get_or_404(topic_id)
    else:
        return "Invalid category", 400

    if request.method == "POST":
        validate_csrf()

        content = request.form.get("content", "").strip()

        if not content:
            return "Content cannot be empty", 400

        if len(content) > 5000:
            return "Content too long", 400

        time.sleep(0.3)

        post = Post(
            content=content,
            user_id=current_user.id,
            topic_id=topic.id,
            topic_type=category
        )
        db.session.add(post)
        db.session.commit()

        return redirect(url_for("main.topic_view", category=category, topic_id=topic.id))

    posts = Post.query.filter_by(
        topic_id=topic.id,
        topic_type=category
    ).order_by(Post.created_at.asc()).all()

    return render_template("topic.html", topic=topic, posts=posts, category=category)


# =========================
# CATEGORY
# =========================

@main_bp.route("/category/<category>")
def category_view(category):
    if category == "red":
        topics = RedTopic.query.order_by(RedTopic.created_at.desc()).all()
    elif category == "blue":
        topics = BlueTopic.query.order_by(BlueTopic.created_at.desc()).all()
    elif category == "purple":
        topics = PurpleTopic.query.order_by(PurpleTopic.created_at.desc()).all()
    else:
        return "Invalid category", 400

    return render_template("category.html", topics=topics, category=category)


# =========================
# INFO ENDPOINT
# =========================

@main_bp.route("/info")
def info():
    mode = os.getenv("APP_MODE")
    if not mode:
        return {"error": "APP_MODE not set"}, 500

    port = os.getenv("PORT")

    data = {
        "app": "mon-api",
        "version": "1.0",
        "mode": mode,
        "port": port,
        "config": {
            "debug": os.getenv("FLASK_DEBUG")
        },
        "python_version": sys.version,
        "hostname": socket.gethostname()
    }

    logging.info(f"/info called - mode={mode}, port={port}")

    return data


# =========================
# RANDOM FAIL
# =========================

@main_bp.route("/random-fail")
def random_fail():
    try:
        if random.randint(1, 3) == 1:  # nosec
            raise Exception("Simulated production bug")

        return {"status": "success", "message": "Request succeeded"}, 200

    except Exception as e:
        current_app.logger.error(f"Random fail triggered: {str(e)}")
        abort(500, description="Internal server error (simulated)")


# =========================
# LOGS DEMO
# =========================

@main_bp.route("/logs-demo")
def logs_demo():
    current_app.logger.info("Request received on /logs-demo")

    if random.random() < 0.5:  # nosec
        current_app.logger.warning("Unusual traffic pattern detected")

    if random.random() < 0.2:  # nosec
        current_app.logger.error("Simulated internal failure")
        return {"error": "internal failure"}, 500

    return {"status": "ok"}, 200


# =========================
# HEALTH CHECK
# =========================

def check_all_routes(app):
    results = {}

    EXCLUDED_ENDPOINTS = {
        "main.google_login",
        "main.google_authorize",
    }

    with app.test_client() as client:
        for rule in app.url_map.iter_rules():

            if "GET" not in rule.methods:
                continue

            if len(rule.arguments) != 0:
                continue

            if rule.rule.startswith(('/static', '/health')):
                continue

            if rule.endpoint in EXCLUDED_ENDPOINTS:
                results[rule.rule] = "SKIPPED_OAUTH"
                continue

            view_func = app.view_functions.get(rule.endpoint)
            if view_func and hasattr(view_func, "__wrapped__"):
                results[rule.rule] = "SKIPPED_AUTH"
                continue

            try:
                response = client.get(rule.rule, follow_redirects=True)
                results[rule.rule] = response.status_code
            except Exception as e:
                results[rule.rule] = f"CRASH: {str(e)}"

    return results


def rollback_deploy():
    """
    Rollback simple basé sur git.
    Reviens au commit précédent et redémarre l'app.
    """

    try:
        current_app.logger.error("ROLLBACK TRIGGERED - restoring previous version")

        subprocess.run(["/usr/bin/git", "reset", "--hard", "HEAD~1"], check=True)

        subprocess.run(["/usr/bin/git", "push", "--force"], check=True)

        subprocess.run(["/usr/bin/systemctl", "restart", "myapp"], check=True)

    except Exception as e:
        current_app.logger.critical(f"Rollback failed: {str(e)}")


@main_bp.route("/health/full")
def full_health_check():
    route_status = check_all_routes(current_app)

    failed = {
        k: v for k, v in route_status.items()
        if v != 200 and not str(v).startswith("SKIPPED")
    }

    status_code = 200
    report = {
        "status": "HEALTHY",
        "timestamp": time.time(),
        "total_checked": len(route_status),
        "details": route_status
    }

    if failed:
        report["status"] = "UNHEALTHY"
        report["anomalies_detected"] = failed
        status_code = 503

        rollback_deploy()

    return report, status_code


@main_bp.route("/admin/config")
def show_config():
    # On va chercher le secret EN DIRECT dans le coffre
    db_pass = get_secret('cyberguard', 'db_password')
    if not db_pass:
        return "Erreur : Coffre-fort inaccessible", 500

    return f"Le mot de passe actuel (récupéré de Vault) est : {db_pass}"
