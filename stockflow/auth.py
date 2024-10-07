from flask import (
    Blueprint, 
    render_template, 
    url_for, 
    request,
    redirect,
    flash
)

from werkzeug.security import generate_password_hash, check_password_hash

# User model
from .models import User

# Database
from stockflow import db

from . import models

bp = Blueprint("auth", __name__, url_prefix="/auth")
# Routes
# Register
@bp.route("/register/", methods = ("GET", "POST"))
def register():
    if request.method == "POST":
        # Get form input values
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        user = User(email, username, generate_password_hash(password))
        
        email = User.query.filter_by(email = email).first() # Get the first value
        username = User.query.filter_by(username = username).first() # Get the first value

        error = None

        # If already exists a user with the email or username
        if email == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        
        elif username == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else: 
            error = f"El usuario {username} ya está registrado"

        flash(error)
        
    return render_template("modules/users/register.html")

# Login
@bp.route("/login/")
def login():
    return render_template("modules/users/login.html")

# Forgot Password
@bp.route("/forgot-password/")
def forgot_password():
    return render_template("modules/users/forgot-password.html")