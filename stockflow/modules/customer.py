from flask import (
    Blueprint, 
    render_template
)

from stockflow.auth import login_required

bp = Blueprint("admin/customers", __name__, url_prefix="/admin/customers")

# Customers
@bp.route("/")
@login_required
def index():
    return render_template("modules/customers/index.html")