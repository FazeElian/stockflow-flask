from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os
from dotenv import load_dotenv

# Load the variables from .env file
load_dotenv()

# Database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Config
    app.config.from_mapping (
        DEBUG = os.getenv("DEBUG_MODE"),
        SECRET_KEY = os.getenv("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    # Initialize the database connection
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

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