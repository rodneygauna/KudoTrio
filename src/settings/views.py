"""
Settings - Views
This file contains the views for the settings blueprint.
"""

# Imports
from datetime import datetime
from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import login_required, current_user
from src.settings.forms import (
    DepartmentForm,
)
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


# Settings - Departments - Add Department
@settings_bp.route("/settings/departments/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_department():
    """
    Add department
    """

    form = DepartmentForm()

    if form.validate_on_submit():
        # Check if department already exists
        if Departments.query.filter_by(name=form.name.data).first():
            flash("Department already exists.", "danger")
            return redirect(url_for("settings.add_department"))

        # Add department
        new_department = Departments(
            name=form.name.data,
            created_date=datetime.now(),
            created_by=current_user.id,
        )
        db.session.add(new_department)
        db.session.commit()

        flash("Department added successfully.", "success")
        return redirect(url_for("settings.view_departments"))

    return render_template("settings/add_edit_department.html",
                           title="Add Department",
                           form=form,
                           )


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
