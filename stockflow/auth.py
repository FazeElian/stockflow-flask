from flask import Blueprint, render_template

from . import models

bp = Blueprint("auth", __name__, url_prefix="/auth")
# Routes
# Register
@bp.route("/register/")
def register():
    return render_template("modules/users/register.html")

# Login
@bp.route("/login/")
def login():
    return render_template("modules/users/login.html")

# Forgot Password
@bp.route("/forgot-password/")
def forgot_password():
    return render_template("modules/users/forgot-password.html")