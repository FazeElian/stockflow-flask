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
@bp.route("/")
@login_required
def index():
    return render_template("modules/inventories/index.html")

# New
@bp.route("/new/", methods=("GET", "POST"))
@login_required
def new():
    # Get all the products that user created
    products = Product.query.filter(Product.created_by == g.user.id).all()

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

    return render_template("modules/inventories/new.html", products = products)