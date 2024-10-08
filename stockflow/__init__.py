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
        SQLALCHEMY_DATABASE_URI="sqlite:///stockflow.db"
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

    # Create database tables
    with app.app_context():
        db.create_all()

    return app