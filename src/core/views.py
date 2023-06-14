"""
Views for the core blueprint
"""


# Imports
from flask import render_template, Blueprint


# Blueprint
core_bp = Blueprint("core", __name__)


# Homepage
@core_bp.route("/")
def index():
    """
    Returns the homepage
    """

    return render_template("core/index.html",
                           title="KudoTrio - Home")
