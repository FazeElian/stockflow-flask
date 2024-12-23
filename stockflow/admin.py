from flask import (
    Blueprint, 
    render_template, 
    request, 
    redirect, 
    url_for,
)

from stockflow.auth import login_required
from werkzeug.utils import secure_filename
import os

bp = Blueprint("admin", __name__, url_prefix="/admin")

# Database
from stockflow import db

# User model
from .models import User

# Routes
# Dashboard
@bp.route("/dashboard/")
@login_required
def dashboard():
    return render_template("modules/dashboard.html")

# Profile
@bp.route("/profile/")
@login_required
def profile():
    return render_template("modules/users/profile/index.html")

# Get user by id
def get_user(id):
    user = User.query.get_or_404(id) # Query to user table
    return user

def get_profile_photo(id):
    user = User.query.get_or_404(id)
    profile_proto = ""
    if profile_proto != "":
        profile_proto = user.profile_photo

    return profile_proto

# Update user - profile
@bp.route("/profile/edit/<int:id>", methods = ("GET", "POST"))
@login_required
def update_user(id):
    # Search on db user id
    user = get_user(id)
    profile_photo = get_profile_photo(id)

    if request.method == "POST":
        user.names = request.form["names"]
        user.last_names = request.form["last_names"]
        user.username = request.form["username"]
        user.email = request.form["email"]

        if "profile_photo" in request.files:
            profile_photo = request.files["profile_photo"]
            
            # Route to save photo
            upload_folder = "stockflow/static/media/user"

            # Check if it already exists
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            # Save photo on a static project folder
            filename = secure_filename(profile_photo.filename)
            profile_photo_path = os.path.join(upload_folder, filename)
            profile_photo.save(profile_photo_path)

            # Save the relative path to the database
            user.profile_photo = f"media/user/{filename}"

        db.session.commit()

        # Redirection
        return redirect(url_for("admin.profile"))

    return render_template("modules/users/profile/edit.html", user = user, profile_photo = profile_photo)