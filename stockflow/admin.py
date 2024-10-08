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

# Category model
from .models import Category

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

# Update user - profile
@bp.route("/profile/edit/<int:id>", methods = ("GET", "POST"))
@login_required
def update_user(id):
    # Search on db user id
    user = get_user(id)

    if request.method == "POST":
        user.names = request.form["names"]
        user.last_names = request.form["last_names"]
        user.username = request.form["username"]
        user.email = request.form["email"]
        user.profile_photo = request.form["profile_photo"]

        db.session.commit()

        # Redirection
        return redirect(url_for("admin.profile"))

    return render_template("modules/users/profile/edit.html", user = user)

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
@bp.route("/products/categories/", methods = ("GET", "POST"))
@login_required
def categories():
    query = ""
    categories = []

    if request.method == "POST":
        query = request.form.get("searchCategorie", "")

        # Filter the categories when the user put a value on the search bar input
        categories = Category.query.filter(
            (
                Category.name.ilike(f"%{query}%") |  # Searching by name
                Category.description.ilike(f"%{query}%")  # Searching by description
            )
        ).all()
    else:
        # Load all the categories where the user is not searching
        categories = Category.query.filter(Category.created_by == g.user.id).all()

    return render_template("modules/products/categories/index.html", categories = categories, query=query)

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