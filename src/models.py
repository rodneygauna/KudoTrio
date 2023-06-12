"""
This file contains the models for the database.
"""


# Imports
from datetime import datetime
from flask import flash, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from src import db, login_manager


# Model - Users
@login_manager.user_loader
def load_user(user_id):
    """
    Returns the user object based on the user id
    """

    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    """
    Redirect unauthorized users to the login page
    """

    flash("You must be logged in to view that page.", "danger")
    return redirect(url_for("users.login"))


class User(db.Model, UserMixin):
    """
    User account model
    """

    __tablename__ = "users"

    # IDs and Foreign Keys
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    # User login information
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # User information
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    role = db.Column(db.String(255))
    status = db.Column(db.String(255), default="active")
    # Change tracking
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    def check_password(self, password):
        """Checks if the password is correct"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username: {self.username}"


class Departments(db.Model):
    """
    Departments model
    """

    __tablename__ = "departments"

    # IDs and Foreign Keys
    id = db.Column(db.Integer, primary_key=True)
    # Department information
    name = db.Column(db.String(255))
    # Change tracking
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"Department: {self.department}"


class Kudo(db.Model):
    """
    Kudos model
    """

    __tablename__ = "kudos"

    # IDs and Foreign Keys
    id = db.Column(db.Integer, primary_key=True)
    submitting_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    receiving_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Kudo information
    kudo_message = db.Column(db.Text)
    # Change tracking
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"Kudo: {self.kudo_message}"
