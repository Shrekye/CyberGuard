import os
import secrets
from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, RedTopic, BlueTopic, PurpleTopic, Post
from authlib.integrations.flask_client import OAuth
from . import db
from . import google

main_bp = Blueprint("main", __name__)

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
        abort(403)

@main_bp.app_context_processor
def inject_csrf():
    return dict(csrf_token=generate_csrf_token())

# =========================
# HOME
# =========================

@main_bp.route("/")
def index():
    red_topics = RedTopic.query.order_by(RedTopic.created_at.desc()).all()
    blue_topics = BlueTopic.query.order_by(BlueTopic.created_at.desc()).all()
    purple_topics = PurpleTopic.query.order_by(PurpleTopic.created_at.desc()).all()
    return render_template("index.html", red_topics=red_topics, blue_topics=blue_topics, purple_topics=purple_topics)

# =========================
# REGISTER
# =========================

@main_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        validate_csrf()

        username = request.form["username"].strip()
        password = generate_password_hash(request.form["password"])

        if User.query.filter_by(username=username).first():
            return "Username already exists!"

        user = User(username=username, password=password)

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

        validate_csrf()

        username = request.form["username"].strip()
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.index"))

        return "Invalid credentials"

    return render_template("login.html")

# =========================
# GOOGLE OAUTH
# =========================

@main_bp.route('/login/google')
def google_login():
    redirect_uri = url_for('main.google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@main_bp.route('/google/auth')
def google_authorize():

    token = google.authorize_access_token()
    user_info = token.get('userinfo')

    if user_info:

        email = user_info['email']
        user = User.query.filter_by(username=email).first()

        if not user:

            user = User(username=email, password="OAUTH_USER")

            db.session.add(user)
            db.session.commit()

        login_user(user)

    return redirect(url_for('main.index'))

# =========================
# LOGOUT
# =========================

@main_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("main.index"))

# =========================
# CREATE TOPIC
# =========================

@main_bp.route("/create_topic", methods=["GET", "POST"])
@login_required
def create_topic():

    if request.method == "POST":

        validate_csrf()

        title = request.form["title"].strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category")

        if not title or category not in ["red", "blue", "purple"]:
            return "Title or category invalid"

        if category == "red":
            topic = RedTopic(title=title, user_id=current_user.id)

        elif category == "blue":
            topic = BlueTopic(title=title, user_id=current_user.id)

        else:
            topic = PurpleTopic(title=title, user_id=current_user.id)

        db.session.add(topic)
        db.session.commit()

        post = Post(
            content=content or "No content",
            user_id=current_user.id,
            topic_id=topic.id,
            topic_type=category
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
        return "Invalid category"

    if request.method == "POST":

        validate_csrf()

        content = request.form.get("content", "").strip()

        if content:

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
        return "Invalid category"

    return render_template("category.html", topics=topics, category=category)