from flask import (
    Blueprint, 
    render_template, 
    request, 
    g, 
    redirect, 
    url_for,
    flash
)

from stockflow.auth import login_required

bp = Blueprint("admin", __name__, url_prefix="/admin")

# Database
from stockflow import db

# Categories models
from .models import Category

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
def new_product():
    return render_template("modules/products/new.html")

# Products Categories
@bp.route("/products/categories/")
@login_required
def categories():
    # Database query
    categories = Category.query.all()

    return render_template("modules/products/categories/index.html", categories = categories)

# New category
@bp.route("/products/categories/new/", methods = ("GET", "POST"))
@login_required
def new_category():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        category = Category(g.user.id, name, description)

        db.session.add(category)
        db.session.commit()

        # Redirection
        return redirect(url_for("admin.categories"))

    return render_template("modules/products/categories/new.html")

# Get category by id
def get_category(id):
    category = Category.query.get_or_404(id)
    return category

# Update category
@bp.route("/products/categories/edit/<int:id>", methods = ("GET", "POST"))
@login_required
def update_category(id):
    # Search on db category id
    category = get_category(id)

    if request.method == "POST":
        category.name = request.form["name"]
        category.description = request.form["description"]

        db.session.commit()

        # Redirection
        return redirect(url_for("admin.categories"))

    return render_template("modules/products/categories/edit.html", category = category)

# Delete category
@bp.route("/products/categories/delete/<int:id>")
@login_required
def delete_category(id):
    category = get_category(id)

    db.session.delete(category)
    db.session.commit()

    # Redirection
    return redirect(url_for("admin.categories"))
    
# Sales
@bp.route("/sales/")
@login_required
def sales():
    return render_template("modules/sales.html")