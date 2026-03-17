from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, RedTopic, BlueTopic, PurpleTopic, Post
from . import db

main_bp = Blueprint("main", __name__)

# --- Home ---
@main_bp.route("/")
def index():
    red_topics = RedTopic.query.order_by(RedTopic.created_at.desc()).all()
    blue_topics = BlueTopic.query.order_by(BlueTopic.created_at.desc()).all()
    purple_topics = PurpleTopic.query.order_by(PurpleTopic.created_at.desc()).all()
    return render_template("index.html", red_topics=red_topics, blue_topics=blue_topics, purple_topics=purple_topics)

# --- Register ---
@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = generate_password_hash(request.form["password"])
        if User.query.filter_by(username=username).first():
            return "Username already exists!"
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("main.login"))
    return render_template("register.html")

# --- Login ---
@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.index"))
        return "Invalid credentials"
    return render_template("login.html")

# --- Logout ---
@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

# --- Create Topic ---
@main_bp.route("/create_topic", methods=["GET", "POST"])
@login_required
def create_topic():
    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category")  # "red", "blue", "purple"
        if not title or category not in ["red", "blue", "purple"]:
            return "Title or category invalid"

        # créer le topic dans la table correspondante
        if category == "red":
            topic = RedTopic(title=title, user_id=current_user.id)
        elif category == "blue":
            topic = BlueTopic(title=title, user_id=current_user.id)
        else:
            topic = PurpleTopic(title=title, user_id=current_user.id)

        db.session.add(topic)
        db.session.commit()

        # créer le premier post
        post = Post(content=content or "No content", user_id=current_user.id,
                    topic_id=topic.id, topic_type=category)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for("main.topic_view", category=category, topic_id=topic.id))

    return render_template("create_topic.html")

# --- View Topic ---
@main_bp.route("/topic/<category>/<int:topic_id>", methods=["GET", "POST"])
@login_required
def topic_view(category, topic_id):
    # récupérer le topic selon sa catégorie
    if category == "red":
        topic = RedTopic.query.get_or_404(topic_id)
    elif category == "blue":
        topic = BlueTopic.query.get_or_404(topic_id)
    elif category == "purple":
        topic = PurpleTopic.query.get_or_404(topic_id)
    else:
        return "Invalid category"

    # ajouter un post si POST
    if request.method == "POST":
        content = request.form.get("content", "").strip()
        if content:
            post = Post(content=content, user_id=current_user.id,
                        topic_id=topic.id, topic_type=category)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("main.topic_view", category=category, topic_id=topic.id))

    posts = Post.query.filter_by(topic_id=topic.id, topic_type=category).order_by(Post.created_at.asc()).all()
    return render_template("topic.html", topic=topic, posts=posts, category=category)