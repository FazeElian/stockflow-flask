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

# Models
# Category model
from .models import Category

# Product model
from .models import Product

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


from werkzeug.utils import secure_filename

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

        if request.files["profile_photo"]:
            profile_photo = request.files["profile_photo"]
            
            # Save photo on a static project folder
            profile_photo.save(f"stockflow/static/media/user/{secure_filename(profile_photo.filename)}") # Get file name
            user.profile_photo = f"media/user/{secure_filename(profile_photo.filename)}"; # Save on db

        db.session.commit()

        # Redirection
        return redirect(url_for("admin.profile"))

    return render_template("modules/users/profile/edit.html", user = user, profile_photo = profile_photo)

# Products
@bp.route("/products/")
@login_required
def products():
    return render_template("modules/products/index.html")

from werkzeug.utils import secure_filename

# def get_image(id):
#     product = Product.query.get_or_404(id)
#     image = ""
#     if image != "":
#         image = product.image

#     return image

# New product
@bp.route("/products/new/", methods=("GET", "POST"))
@login_required
def new_product():
    # Get all the categories that user created
    categories = Category.query.filter(Category.created_by == g.user.id).all()
    image = None

    if request.method == "POST":
        name = request.form["name"]
        code = request.form["code"]
        category = request.form["category"]
        price = request.form["price"]

        if "image" in request.files and request.files["image"]:
            uploaded_image = request.files["image"]
            
            filename = secure_filename(uploaded_image.filename)
            uploaded_image.save(f"stockflow/static/media/product/{filename}")  # Guarda el archivo
            image = f"media/product/{filename}"  # Guarda la URL en la variable

        # Crea el nuevo producto
        product = Product(g.user.id, name, code, category, price, image)

        # Agrega el producto a la base de datos
        db.session.add(product)
        db.session.commit()

        # Redirección
        return redirect(url_for("admin.products"))

    return render_template("modules/products/new.html", categories=categories, image=image)

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