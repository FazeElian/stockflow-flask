from flask import (
    Blueprint, 
    render_template, 
    request, 
    g, 
    redirect, 
    url_for
)

from stockflow.auth import login_required

bp = Blueprint("admin/products/categories", __name__, url_prefix="/admin/products/categories")

# Database
from stockflow import db

# Models
from stockflow.models import Category

# Products Categories
@bp.route("/", methods = ("GET", "POST"))
@login_required
def index():
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
@bp.route("/new/", methods = ("GET", "POST"))
@login_required
def new():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        category = Category(g.user.id, name, description)

        db.session.add(category)
        db.session.commit()

        # Redirection
        return redirect(url_for("admin/products/categories.index"))

    return render_template("modules/products/categories/new.html")

# Get category by id
def get_category(id):
    category = Category.query.get_or_404(id)
    return category

# Update category
@bp.route("/edit/<int:id>", methods = ("GET", "POST"))
@login_required
def update(id):
    # Search on db category id
    category = get_category(id)

    if request.method == "POST":
        category.name = request.form["name"]
        category.description = request.form["description"]

        db.session.commit()

        # Redirection
        return redirect(url_for("admin/products/categories.index"))

    return render_template("modules/products/categories/edit.html", category = category)

# Delete category
@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    category = get_category(id)

    db.session.delete(category)
    db.session.commit()

    # Redirection
    return redirect(url_for("admin/products/categories.index"))