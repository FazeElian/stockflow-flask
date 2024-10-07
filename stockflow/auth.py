from flask import Blueprint

bp = Blueprint("auth", __name__, url_prefix="/auth")
# Routes
# Register
@bp.route("/register/")
def register():
    return "Register view"

# Login
@bp.route("/login/")
def login():
    return "Login view"

# Forgot Password
@bp.route("/forgot-password/")
def forgot_password():
    return "Forgot Password view"