"""
Users - Views
This file contains the views for the users blueprint.
"""

# Imports
import random
import string
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from flask_mail import Message
from src import db, mail
from src.users.forms import (
    LoginForm,
    UserForm,
)
from src.models import User
from src.decorators.decorators import admin_required


# Blueprint Configuration
users_bp = Blueprint("users", __name__)


# Login
@users_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Logs in a user
    """

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Successful login
        if user is not None and user.check_password(form.password.data):
            login_user(user)

            next = request.args.get('next')

            if next is None or not next[0] == '/':
                next = url_for('core.index')

            flash('Login successful.', 'success')
            return redirect(next)
        # Unsuccessful login
        flash('Invalid email or password.', 'danger')
        return redirect(url_for('users.login'))

    return render_template('users/login.html',
                           title='Login',
                           form=form)


# Logout user
@users_bp.route('/logout')
@login_required
def logout():
    '''Logs out a user'''

    logout_user()
    return redirect(url_for('core.index'))


# Form - Add user
@users_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    """
    User add form
    """

    form = UserForm()

    if form.validate_on_submit():
        # Get form data
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        department = form.department.data
        role = form.role.data

        # Checks if email is already registered
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('users.add_user'))

        # Generate a random password
        rand_password = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=12)
        )

        # Adds user to database
        new_user = User(
            email=email,
            password_hash=generate_password_hash(
                rand_password, method='sha256'),
            firstname=firstname,
            lastname=lastname,
            department=department,
            role=role,
            status="active",
            created_date=datetime.utcnow(),
            created_by=current_user.id,
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully.', 'success')

        # Send email to new user
        msg = Message(
            "H30 Product App - New User",
            recipients=[email],
            sender="noreply@healthtrio.com",
        )
        msg.body = f"""
        Hello {firstname},

        You have been added as a user.

        Your login email is: {email}

        Your temporary password is: {rand_password}

        Please login and change your password.
        {url_for('users.login', _external=True)}
        """
        mail.send(msg)

        return redirect(url_for('core.index'))

    return render_template('users/add_user.html',
                           title='Add User',
                           form=form)
