"""
Settings - Views
This file contains the views for the settings blueprint.
"""

# Imports
from datetime import datetime
from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import func
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

    return render_template("settings/settings.html", title="Settings")


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

    return render_template(
        "settings/departments.html",
        title="Departments",
        departments=departments,
        department_user_count=department_user_count,
    )


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
        department_name = form.name.data.lower()
        if Departments.query.filter(
            func.lower(Departments.name) == department_name
        ).first():
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

    return render_template(
        "settings/add_edit_department.html",
        title="Add Department",
        form=form,
    )


# Settings - Departments - Edit Department
@settings_bp.route(
    "/settings/departments/edit/<int:department_id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def edit_department(department_id):
    """
    Edit department
    """

    form = DepartmentForm()

    # Get department
    department = Departments.query.get_or_404(department_id)

    # Populate form fields
    if request.method == "GET":
        form.name.data = department.name

        return render_template(
            "settings/add_edit_department.html",
            title="Edit Department",
            form=form,
        )

    if form.validate_on_submit():
        # Check if department already exists
        department_name = form.name.data.lower()
        if Departments.query.filter(
            func.lower(Departments.name) == department_name
        ).first():
            flash("Department already exists.", "danger")
            return redirect(url_for("settings.edit_department",
                                    department_id=department_id))

        # Update department
        try:
            department.name = form.name.data
            department.updated_date = datetime.now()
            department.updated_by = current_user.id
            db.session.commit()
            flash("Department updated successfully.", "success")
        except Exception as e:
            flash(f"Error updating department. Error: {e}", "danger")
            return redirect(url_for("settings.edit_department",
                                    department_id=department_id))

        return redirect(url_for("settings.view_departments"))


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
        db.session.query(User.id).filter_by(
            department_id=department_id
            ).count()
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

    return render_template(
        "settings/view_department_details.html",
        title="Department Details",
        department=department,
        department_user_count=department_user_count,
        department_users=department_users,
    )


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
            User.status,
            Departments.name,
        )
        .outerjoin(Departments, User.department_id == Departments.id)
        .order_by(User.lastname)
        .all()
    )

    return render_template("settings/users.html", title="Users", users=users)
