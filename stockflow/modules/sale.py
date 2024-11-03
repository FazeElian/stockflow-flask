from flask import (
    Blueprint, 
    render_template,
    request,
    url_for,
    redirect,
    g
)

from stockflow.auth import login_required

bp = Blueprint("admin/sales", __name__, url_prefix="/admin/sales")

# Database
from stockflow import db

# Models
from stockflow.models import Sale, Product, SaleItem, Customer

# Sales
@bp.route("/")
@login_required
def index():
    sales = Sale.query.filter(Sale.created_by == g.user.id).all()

    return render_template("modules/sales/index.html", sales = sales)

# View sale
@bp.route("/view/<int:id>")
@login_required
def view(id):
    # Get sale by id
    sale = get_sale(id)

    # Get all the product items associated with the sale
    sale_items = SaleItem.query.filter_by(sale_id=sale.id).all()

    return render_template("modules/sales/view.html", sale = sale, sale_items = sale_items)

# New sale
@bp.route("/new/", methods=("GET", "POST"))
@login_required
def new():
    # Obtener todos los productos
    products = Product.query.filter(Product.created_by == g.user.id).all()

    # Obtener todos los clientes
    customers = Customer.query.filter(Customer.created_by == g.user.id).all()

    if request.method == "POST":
        customer_id = request.form["customer"]

        if customer_id == "default" or not customer_id:
            customer_id = None

        # Create the new sale without products
        sale = Sale(
            created_by = g.user.id,
            customer_id=customer_id,
            date = request.form["date"],
            total = 0
        )
    
        # Get the products selected and quantities
        selected_products = request.form.getlist("products")
        quantities = request.form.getlist("quantity")

        # Add the sale
        db.session.add(sale)
        db.session.commit()

        # Calculate the total sale
        total_sale = 0

        # Add the products list to sale using the id
        for index, product_id in enumerate(selected_products):
            product = Product.query.get(product_id)
            quantity = int(quantities[index])

            # Create a new sale item
            sale_item = SaleItem(
                created_by=g.user.id,
                sale_id=sale.id, 
                product_id=product.id, 
                quantity=quantity, 
                price=product.price
            )

            # Product total
            total_sale += product.price * quantity

            # Add the sale item
            db.session.add(sale_item)

        # Update the total sale value
        sale.total = total_sale
        db.session.commit() # Save all

        # Redirection
        return redirect(url_for("admin/sales.index"))

    return render_template("modules/sales/new.html", products = products, customers = customers)

# Get sale by id
def get_sale(id):
    sale = Sale.query.get_or_404(id)
    return sale

# Delete sale
@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    sale = get_sale(id)
    
    # Eliminar los elementos de venta relacionados (SaleItem)
    SaleItem.query.filter_by(sale_id=sale.id).delete()
    
    # Eliminar la venta
    db.session.delete(sale)
    db.session.commit()

    # Redirección a la lista de ventas
    return redirect(url_for("admin/sales.index"))

def update(id):
    # Fetch the sale by ID
    sale = Sale.query.get_or_404(id)

    # Fetch the SaleItems associated with the sale
    sale_items = SaleItem.query.filter_by(sale_id=sale.id).all()

    # Fetch all products created by the user
    products = Product.query.filter(Product.created_by == g.user.id).all()

    # Fetch all customers created by the user
    customers = Customer.query.filter(Customer.created_by == g.user.id).all()

    if request.method == "POST":
        # Fetch the customer_id from the form
        customer_id = request.form.get("customer")

        # Validate that customer_id is valid
        if customer_id == "default" or not customer_id:
            customer_id = None  # Allow None if no customer is selected

        # Update the sale with data from the form
        sale.customer_id = customer_id  # This can be None if no customer is selected
        sale.date = request.form.get("date")

        # Fetch the new items selected from the form
        selected_products = request.form.getlist("sale_items")
        quantities = request.form.getlist("quantity")

        # Calculate the total of the sale
        sale.total = sale.total;

        # Create a dictionary to map the selected products and their quantities
        selected_data = {int(product_id): int(quantity) for product_id, quantity in zip(selected_products, quantities)}

        for product_id, quantity in selected_data.items():
            sale_item = SaleItem.query.filter_by(sale_id=sale.id, product_id=product_id).first()

            if sale_item:
                # If the item already exists, update the quantity
                sale_item.quantity = quantity
            else:
                # If the item doesn't exist, create a new SaleItem
                product = Product.query.get(product_id)
                sale_item = SaleItem(
                    created_by=g.user.id,
                    sale_id=sale.id,
                    product_id=product_id,
                    quantity=quantity,
                    price=product.price
                )

                db.session.add(sale_item)

            # Add to the total
            total_sale = sale_item.price * quantities

            # Update the total of the sale
            sale.total = total_sale

        # Update the total of the sale
        # sale.total = total_sale

        # Save the changes to the database
        db.session.commit()

        # Redirect to the sales list
        return redirect(url_for("admin/sales.index"))

    # Render the template with the products of the sale and all available products
    return render_template("modules/sales/edit.html", sale=sale, sale_items=sale_items, products=products, customers=customers)
