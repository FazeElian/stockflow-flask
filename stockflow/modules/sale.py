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

# New sale
@bp.route("/new/", methods=("GET", "POST"))
@login_required
def new():
    # Obtener todos los productos
    products = Product.query.filter(Product.created_by == g.user.id).all()

    # Obtener todos los clientes
    customers = Customer.query.filter(Product.created_by == g.user.id).all()

    if request.method == "POST":
        # Create the new sale without products
        sale = Sale(
            created_by = g.user.id,
            customer_id = request.form["customer"],
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