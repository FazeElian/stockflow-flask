from flask import Blueprint, render_template
from stockflow.auth import login_required

bp = Blueprint("admin", __name__, url_prefix="/admin")

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
    return render_template("modules/users/profile.html")

# Products
@bp.route("/products/")
@login_required
def products():
    return render_template("modules/products/index.html")

# New product
@bp.route("/products/new/")
@login_required
def new():
    return render_template("modules/products/new.html")

# Sales
@bp.route("/sales/")
@login_required
def sales():
    return render_template("modules/sales.html")