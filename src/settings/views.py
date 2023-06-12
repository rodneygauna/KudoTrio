"""
Settings - Views
This file contains the views for the settings blueprint.
"""

# Imports
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required, current_user
from src.models import (
    User,
    Departments,
)
from src import db
from src.decorators.decorators import admin_required
from src.settings.get_department_user_count import get_department_user_count


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


# Settings - Departments - View List of Departments
@settings_bp.route("/settings/departments")
@login_required
@admin_required
def view_departments():
    """
    View departments
    """

    # Get all departments
    departments = Departments.query.order_by(Departments.name.asc()).all()

    # Get total count of users for each department
    department_user_count = get_department_user_count()

    return render_template("settings/departments.html",
                           title="Departments",
                           departments=departments,
                           department_user_count=department_user_count)


# Settings - Departments - View Department Details
@settings_bp.route("/settings/departments/<int:department_id>")
@login_required
@admin_required
def view_department_details(department_id):
    """
    View department details
    """

    # Get department
    department = Departments.query.get_or_404(department_id)

    # Get total count of users for each department
    department_user_count = (
        db.session.query(User.id)
        .filter_by(department_id=department_id).count()
    )

    # Get user details for the department
    department_users = (
        db.session.query(
            User.id,
            User.firstname,
            User.lastname,
            User.email,
            User.status,
            User.department_id,
        )
        .filter_by(department_id=department_id)
        .order_by(User.lastname)
        .all()
    )

    return render_template("settings/view_department_details.html",
                           title="Department Details",
                           department=department,
                           department_user_count=department_user_count,
                           department_users=department_users)


# Settings - Users
@settings_bp.route("/settings/users")
@login_required
@admin_required
def settings_users():
    """
    Settings for users
    """

    users = (
        db.session.query(
            User.id,
            User.firstname,
            User.lastname,
            User.department_id,
            Departments.name,
        )
        .outerjoin(Departments, User.department_id == Departments.id)
        .order_by(User.lastname)
        .all()
    )

    return render_template("settings/users.html",
                           title="Users",
                           users=users)
