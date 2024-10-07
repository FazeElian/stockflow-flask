from flask import (
    Blueprint, 
    render_template, 
    url_for, 
    request,
    redirect,
    flash,
    session, # Save the user who start a session
    g # Save any value (for example: cookies)
)

from werkzeug.security import generate_password_hash, check_password_hash

# User model
from .models import User

# Database
from stockflow import db

from . import models

# Session protected routes
import functools

def login_required(view):
    @functools.wraps(view)

    def wrapped_view(**kwargs):
        if g.user is None:
            message = "Debes iniciar sesión"
            flash(message)

            # Redirection
            return redirect(url_for("auth.login"))
        
        return view(**kwargs)
    return wrapped_view

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
@bp.route("/login/", methods = ("GET", "POST"))
def login():
    if request.method == "POST":
        # Get form input values
        username = request.form["username"]
        password = request.form["password"]

        error = None

        user = User.query.filter_by(username = username).first()

        if user == None:
            error = "Nombre de usuario incorrecto"
        elif not check_password_hash(user.password, password):
            error = "Contraseña incorrecta"

        # Log in
        if error == None:
            session.clear()
            # Key
            session["user_id"] = user.id
            return redirect(url_for("admin.dashboard"))
        
        flash(error)

    return render_template("modules/users/login.html")

@bp.before_app_request # Execute the next function in every request, every page
def load_logged_in_user():
    # Session user id
    user_id = session.get("user_id")
    
    # Save the object with a null value
    if user_id is None:
        g.user = None
    # Return a user after a query
    else:
        g.user = User.query.get_or_404(user_id)

# Log out
@bp.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("index"))

# Forgot Password
@bp.route("/forgot-password/")
def forgot_password():
    return render_template("modules/users/forgot-password.html")