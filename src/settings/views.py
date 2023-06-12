"""
Settings - Views
This file contains the views for the settings blueprint.
"""

# Imports
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required, current_user
from src.models import (
    User
)
from src.decorators.decorators import admin_required


# Blueprint Configuration
settings_bp = Blueprint("settings", __name__)


# Settings - Landing Page
@settings_bp.route("/settings")
@login_required
@admin_required
def settings_landing_page():
    """
    Landing page for settings
    """

    return render_template("settings/settings.html",
                           title="Settings")


# Settings - Users
@settings_bp.route("/settings/users")
@login_required
@admin_required
def settings_users():
    """
    Settings for users
    """

    users = User.query.all()

    return render_template("settings/users.html",
                           title="Users",
                           users=users)
