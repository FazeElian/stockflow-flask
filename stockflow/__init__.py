from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    # Config
    app.config.from_mapping (
        DEBUG = True,
        SECRET_KEY = "dev"
    )

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

    return app