from flask import (
    Blueprint, 
    render_template, 
    request, 
    g, 
    redirect, 
    url_for
)

from stockflow.auth import login_required

bp = Blueprint("admin/customers", __name__, url_prefix="/admin/customers")

# Database
from stockflow import db

# Models
from stockflow.models import Customer

# Customers
@bp.route("/", methods = ("GET", "POST"))
@login_required
def index():
    query = ""
    customers = []

    if request.method == "POST":
        query = request.form.get("searchCustomer", "")

        # Filter the customers when the user put a value on the search bar input
        customers = Customer.query.filter(
            (
                Customer.name.ilike(f"%{query}%") |  # Searching by name
                Customer.description.ilike(f"%{query}%")  # Searching by description
            )
        ).all()
    else:
        # Load all the customers where the user is not searching
        customers = Customer.query.filter(Customer.created_by == g.user.id).all()

    return render_template("modules/customers/index.html", customers = customers, query=query)

# New customer
@bp.route("/new/", methods = ("GET", "POST"))
@login_required
def new():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        customer = Customer(g.user.id, name, description)

        db.session.add(customer)
        db.session.commit()

        # Redirection
        return redirect(url_for("admin/customers.index"))

    return render_template("modules/customers/new.html")

# Get customer by id
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer

# Update customer
@bp.route("/edit/<int:id>", methods = ("GET", "POST"))
@login_required
def update(id):
    # Search on db Customer id
    customer = get_customer(id)

    if request.method == "POST":
        customer.name = request.form["name"]
        customer.description = request.form["description"]

        db.session.commit()

        # Redirection
        return redirect(url_for("admin/customers.index"))

    return render_template("modules/customers/edit.html", customer = customer)

# Delete Customer
@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    customer = get_customer(id)

    db.session.delete(customer)
    db.session.commit()

    # Redirection
    return redirect(url_for("admin/customers.index"))