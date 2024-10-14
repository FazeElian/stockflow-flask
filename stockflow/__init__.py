from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Config
    app.config.from_mapping (
        DEBUG = True,
        SECRET_KEY = "dev",
        SQLALCHEMY_DATABASE_URI="mysql+pymysql://root@localhost/db_stockflow",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Initialize the database connection
    db.init_app(app)

    # Index
    @app.route("/")
    def index():
        return render_template("index.html")

    # Admin views blueprint
    from . import admin
    app.register_blueprint(admin.bp)

    # Auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # Product blueprint
    from stockflow.modules import product
    app.register_blueprint(product.bp)

    # Products Category blueprint
    from stockflow.modules import category
    app.register_blueprint(category.bp)

    # Inventories blueprint
    from stockflow.modules import inventory
    app.register_blueprint(inventory.bp)

    # Sales blueprint
    from stockflow.modules import sale
    app.register_blueprint(sale.bp)

    # Customers blueprint
    from stockflow.modules import customer
    app.register_blueprint(customer.bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app