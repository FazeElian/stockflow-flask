from flask import (
    Blueprint, 
    render_template, 
    request, 
    g, 
    redirect, 
    url_for
)

from stockflow.auth import login_required
from werkzeug.utils import secure_filename
import os

bp = Blueprint("admin/products", __name__, url_prefix="/admin/products")

# Database
from stockflow import db

# Models
from stockflow.models import Product
from stockflow.models import Category

# Products main view
@bp.route("/", methods = ("GET", "POST"))
@login_required
def index():
    query = ""
    products = []

    if request.method == "POST":
        query = request.form.get("searchProduct", "")

        # Filter the products when the user put a value on the search bar input
        products = Product.query.filter(
            (
                Product.name.ilike(f"%{query}%") |  # Searching by name
                Product.code.ilike(f"%{query}%")  # Searching by code
            )
        ).all()
    else:
        # Load all the products where the user is not searching
        products = Product.query.filter(Product.created_by == g.user.id).all()

    return render_template("modules/products/index.html", products = products, query=query)

# New product
@bp.route("/new/", methods=("GET", "POST"))
@login_required
def new():
    # Get all categories created by the user
    categories = Category.query.filter(Category.created_by == g.user.id).all()
    image = None

    if request.method == "POST":
        # Get form data
        name = request.form["name"]
        code = request.form["code"]
        category_id = request.form["category"]
        price = request.form["price"]

        # Check if an image was uploaded
        if "image" in request.files:
            image = request.files["image"]

            # Define the upload folder
            upload_folder = "stockflow/static/media/product"
            # Check if the folder exists, if not, create it
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            # Save the image with a secure filename
            filename = secure_filename(image.filename)
            image_path = os.path.join(upload_folder, filename)
            image.save(image_path)  # Save the image file
            image = f"media/product/{filename}"  # Save relative path to image

        # Create the new product
        product = Product(g.user.id, name, code, category_id, price, image)

        # Add the product to db
        db.session.add(product)
        db.session.commit()

        return redirect(url_for("admin/products.index"))

    return render_template("modules/products/new.html", categories=categories, image=image)

# Get product by id
def get_product(id):
    product = Product.query.get_or_404(id)
    return product

def get_product_image(id):
    product = Product.query.get_or_404(id)
    product_img = ""
    if product_img != "":
        product_img = product.image

    return product_img

# Update product
@bp.route("/edit/<int:id>", methods=("GET", "POST"))
@login_required
def update(id):
    # Get product by ID
    product = get_product(id)
    # Get all categories created by the user
    categories = Category.query.filter(Category.created_by == g.user.id).all()

    if request.method == "POST":
        # Update product details
        product.name = request.form["name"]
        product.code = request.form["code"]
        product.category_id = request.form["category"]
        product.price = request.form["price"]

        # Check if a new image was uploaded
        if "image" in request.files:
            image = request.files["image"]

            # Define the upload folder
            upload_folder = "stockflow/static/media/product"
            # Check if the folder exists, if not, create it
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            # Save the image with a secure filename
            filename = secure_filename(image.filename)
            image_path = os.path.join(upload_folder, filename)
            image.save(image_path)  # Save the image file
            product.image = f"media/product/{filename}"  # Update path in the database

        # Commit changes to the database
        db.session.commit()

        return redirect(url_for("admin/products.index"))

    return render_template("modules/products/edit.html", product=product, categories=categories)

# Delete product
@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    product = get_product(id)

    db.session.delete(product)
    db.session.commit()

    # Redirection
    return redirect(url_for("admin/products.index"))