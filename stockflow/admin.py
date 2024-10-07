from flask import Blueprint, render_template

bp = Blueprint("admin", __name__, url_prefix="/admin")

# Routes
# Dashboard
@bp.route("/dashboard/")
def dashboard():
    return render_template("modules/dashboard.html")

# Profile
@bp.route("/profile/")
def profile():
    return render_template("modules/users/profile.html")

# Products
@bp.route("/products/")
def products():
    return render_template("modules/products.html")

# sSles
@bp.route("/sales/")
def sales():
    return render_template("modules/sales.html")