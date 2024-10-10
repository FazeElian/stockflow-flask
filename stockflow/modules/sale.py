from flask import (
    Blueprint, 
    render_template
)

from stockflow.auth import login_required

bp = Blueprint("admin/sales", __name__, url_prefix="/admin/sales")

# Sales
@bp.route("/")
@login_required
def index():
    return render_template("modules/sales/index.html")

# New sale
@bp.route("/new/")
@login_required
def new():
    return render_template("modules/sales/new.html")