from flask import (
    Blueprint, 
    render_template
)

from stockflow.auth import login_required

bp = Blueprint("admin/inventories", __name__, url_prefix="/admin/inventories")

# Inventories
@bp.route("/")
@login_required
def index():
    return render_template("modules/inventories/index.html")