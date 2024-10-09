from flask import (
    Blueprint, 
    render_template,
    request,
    g,
    redirect,
    url_for
)

from stockflow.auth import login_required

bp = Blueprint("admin/inventories", __name__, url_prefix="/admin/inventories")

# Database
from stockflow import db

# Models
from stockflow.models import Inventory
from stockflow.models import Product

# Inventories
@bp.route("/", methods = ("GET", "POST"))
@login_required
def index():
    query = ""
    inventories = []

    if request.method == "POST":
        query = request.form.get("searchInventory", "")

        # Filter inventories by product name or product code
        inventories = Inventory.query.join(Product).filter(
            (
                Product.name.ilike(f"%{query}%") |  # Searching by product name
                Product.code.ilike(f"%{query}%")    # Searching by product code
            )
        ).all()
    else:
        # Load all the inventories where the user is not searching
        inventories = Inventory.query.filter(Inventory.created_by == g.user.id).all()

    return render_template("modules/inventories/index.html", inventories = inventories, query=query)

# New
@bp.route("/new/", methods=("GET", "POST"))
@login_required
def new():
    # Get all the products that user created
    products = Product.query.filter(Product.created_by == g.user.id).all()

    # Get the ids of the products on inventory
    inventory_prods_ids = [item.product_id for item in Inventory.query.all()]

    # Filter the products that aren't on inventory
    available_products = [product for product in products if product.id not in inventory_prods_ids]

    if request.method == "POST":
        product_id = request.form["product"]
        inflows = request.form["inflows"]

        # Create the new inventory
        inventory = Inventory(g.user.id, product_id, inflows)

        # Add the product to db
        db.session.add(inventory)
        db.session.commit()

        # Redirection
        return redirect(url_for("admin/inventories.index"))

    return render_template("modules/inventories/new.html", products = available_products)

# Get inventory by id
def get_inventory(id):
    inventory = Inventory.query.get_or_404(id)
    return inventory

# Update inventory
@bp.route("/edit/<int:id>", methods = ("GET", "POST"))
@login_required
def update(id):
    # Search on db inventory id
    inventory = get_inventory(id)

    if request.method == "POST":
        inventory.inflows = int(request.form["inflows"])

        # Update stock
        inventory.stock = inventory.inflows - inventory.outflows

        db.session.commit()

        # Redirection
        return redirect(url_for("admin/inventories.index"))

    return render_template("modules/inventories/edit.html", inventory = inventory)

# Delete inventory
@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    inventory = get_inventory(id)

    db.session.delete(inventory)
    db.session.commit()

    # Redirection
    return redirect(url_for("admin/inventories.index"))