from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    # Config
    app.config.from_mapping (
        DEBUG = True,
        SECRET_KEY = "dev"
    )

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/dashboard/")
    def dashboard():
        return render_template("modules/dashboard.html")
    
    return app