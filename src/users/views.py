"""
Users - Views
This file contains the views for the users blueprint.
"""

# Imports
import random
import string
import csv
import os
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Message
from src import db, mail
from src.users.forms import (
    LoginForm,
    UserForm,
    UserRegistrationForm,
    ChangePasswordForm,
    ChangeUserStatusForm,
)
from src.models import (
    User,
    Departments,
    Kudo,
)
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


# Users - User Registration
@users_bp.route('/register', methods=['GET', 'POST'])
def user_registration():
    """
    User registration form
    """

    form = UserRegistrationForm()

    # Department choices
    department_choices = db.session.query(
        Departments.id, Departments.name
    ).order_by(Departments.name.asc()).all()

    form.department.choices = [
        (department.id, department.name) for department in department_choices
    ]

    if form.validate_on_submit():
        # Get form data
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        department_id = form.department.data
        password = generate_password_hash(form.password.data)

        # Checks if email is already registered
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('users.add_user'))

        # Adds user to database
        new_user = User(
            email=email,
            password_hash=password,
            firstname=firstname,
            lastname=lastname,
            department_id=department_id,
            role="user",
            status="active",
            created_date=datetime.utcnow(),
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registered successfully.', 'success')

        return redirect(url_for('users.login'))

    return render_template('users/registration.html',
                           title='User Registration',
                           form=form)


# Form - Add user
@users_bp.route('/settings/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    """
    User add form
    """

    form = UserForm()

    # Department choices
    department_choices = db.session.query(
        Departments.id, Departments.name
    ).order_by(Departments.name.asc()).all()

    form.department.choices = [
        (department.id, department.name) for department in department_choices
    ]

    if form.validate_on_submit():
        # Get form data
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        department_id = form.department.data
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
                rand_password),
            firstname=firstname,
            lastname=lastname,
            department_id=department_id,
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
            "KudoTrio - New User",
            recipients=[email],
            sender="noreply@healthtrio.com",
        )
        msg.body = f"""
        Hello {firstname},

        You have been added as a user.

        Your login email is:
        {email}

        Your temporary password is:
        {rand_password}

        Please login and change your password.
        {url_for('users.login', _external=True)}
        """
        mail.send(msg)

        return redirect(url_for('core.index'))

    return render_template('users/add_user.html',
                           title='Add User',
                           form=form)


# Users - Change Password
@users_bp.route('/change_password/<int:user_id>',
                methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    """
    Change user password
    """

    form = ChangePasswordForm()

    # Get user
    user = User.query.get_or_404(user_id)

    if current_user.id != user.id:
        return "You are not authorized to view this page.", 401

    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        user.updated_date = datetime.utcnow()
        user.updated_by = current_user.id
        db.session.commit()
        flash('Password changed successfully.', 'success')
        return redirect(url_for('core.index'))

    return render_template('users/change_password.html',
                           title='Change Password',
                           form=form,
                           user=user)


# Users - Force Password Change
@users_bp.route('/settings/force_password_change/<int:user_id>',
                methods=['POST'])
@login_required
@admin_required
def force_password_change(user_id):
    """
    Force password change
    """

    # Get user
    user = User.query.get_or_404(user_id)

    # Change user status
    if request.method == 'POST':

        # Generate a random password
        rand_password = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=12)
        )

        user.password_hash = generate_password_hash(rand_password)
        user.updated_date = datetime.utcnow()
        user.updated_by = current_user.id
        db.session.commit()
        flash('User password changed successfully.', 'success')

        # Send email to new user
        msg = Message(
            "KudoTrio - Forced Password Change",
            recipients=[user.email],
            sender="noreply@healthtrio.com",
        )
        msg.body = f"""
        Hello {user.firstname},

        You're password has been changed by an administrator.

        Your temporary password is:
        {rand_password}

        Please login and change your password.
        {url_for('users.login', _external=True)}
        """
        mail.send(msg)

        return redirect(url_for('settings.settings_users'))


# Users - Change Status
@users_bp.route('/settings/change_status/<int:user_id>',
                methods=['GET', 'POST'])
@login_required
@admin_required
def change_status(user_id):
    """
    Changes user status
    """

    form = ChangeUserStatusForm()

    # Get user
    user = User.query.get_or_404(user_id)

    # Set form status to current user status
    if request.method == 'GET':
        form.status.data = user.status

    # Change user status
    if form.validate_on_submit():
        user.status = form.status.data
        user.updated_date = datetime.utcnow()
        user.updated_by = current_user.id
        db.session.commit()
        flash(f'User status changed to {user.status} successfully.', 'success')
        return redirect(url_for('core.index'))

    return render_template('users/change_status.html',
                           title='Change User Status',
                           form=form,
                           user=user)


# Users - Profile
@users_bp.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    """
    User profile
    """

    # Get user
    user = User.query.get_or_404(user_id)

    # Get Kudos
    CreatingUser = db.aliased(User, name="CreatingUser")
    CreatingUserDepartment = db.aliased(
        Departments, name="CreatingUserDepartment")
    ReceivingUser = db.aliased(User, name="ReceivingUser")
    ReceivingUserDepartment = db.aliased(
        Departments, name="ReceivingUserDepartment")

    kudos_submitted = (
        db.session.query(
            Kudo.id,
            Kudo.submitting_user_id,
            Kudo.receiving_user_id,
            Kudo.kudo_message,
            Kudo.created_date,
            CreatingUser.firstname.label("creating_user_firstname"),
            CreatingUser.lastname.label("creating_user_lastname"),
            CreatingUser.department_id,
            CreatingUserDepartment.name.label("creating_user_department_name"),
            ReceivingUser.firstname.label("receiving_user_firstname"),
            ReceivingUser.lastname.label("receiving_user_lastname"),
            ReceivingUser.department_id,
            ReceivingUserDepartment.name.label(
                "receiving_user_department_name"),
        )
        .outerjoin(CreatingUser,
                   CreatingUser.id == Kudo.submitting_user_id)
        .outerjoin(CreatingUserDepartment,
                   CreatingUserDepartment.id == CreatingUser.department_id)
        .outerjoin(ReceivingUser,
                   ReceivingUser.id == Kudo.receiving_user_id)
        .outerjoin(ReceivingUserDepartment,
                   ReceivingUserDepartment.id == ReceivingUser.department_id)
        .filter(Kudo.submitting_user_id == user_id)
        .order_by(Kudo.created_date.desc())
        .limit(10)
    )

    kudos_received = (
        db.session.query(
            Kudo.id,
            Kudo.submitting_user_id,
            Kudo.receiving_user_id,
            Kudo.kudo_message,
            Kudo.created_date,
            CreatingUser.firstname.label("creating_user_firstname"),
            CreatingUser.lastname.label("creating_user_lastname"),
            CreatingUser.department_id,
            CreatingUserDepartment.name.label("creating_user_department_name"),
            ReceivingUser.firstname.label("receiving_user_firstname"),
            ReceivingUser.lastname.label("receiving_user_lastname"),
            ReceivingUser.department_id,
            ReceivingUserDepartment.name.label(
                "receiving_user_department_name"),
        )
        .outerjoin(CreatingUser,
                   CreatingUser.id == Kudo.submitting_user_id)
        .outerjoin(CreatingUserDepartment,
                   CreatingUserDepartment.id == CreatingUser.department_id)
        .outerjoin(ReceivingUser,
                   ReceivingUser.id == Kudo.receiving_user_id)
        .outerjoin(ReceivingUserDepartment,
                   ReceivingUserDepartment.id == ReceivingUser.department_id)
        .filter(Kudo.receiving_user_id == user_id)
        .order_by(Kudo.created_date.desc())
        .limit(10)
    )

    return render_template('users/profile.html',
                           title='User Profile',
                           user=user,
                           kudos_submitted=kudos_submitted,
                           kudos_received=kudos_received)


# Users - Edit Profile
@users_bp.route('/edit_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    """
    Edit user profile
    """

    form = UserForm()

    # Department choices
    department_choices = db.session.query(
        Departments.id, Departments.name
    ).order_by(Departments.name.asc()).all()

    form.department.choices = [
        (department.id, department.name) for department in department_choices
    ]

    # Get user
    user = User.query.get_or_404(user_id)

    if request.method == 'GET':
        # Set form data to current user data
        form.email.data = user.email
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.department.data = user.department_id
        form.role.data = user.role

    if form.validate_on_submit():
        # Checks if email is being changed and is already registered
        if user.email != form.email.data:
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered.', 'danger')
                return redirect(url_for('users.edit_profile', user_id=user.id))

        # Update user
        user.email = form.email.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.department_id = form.department.data
        user.role = form.role.data
        user.updated_date = datetime.utcnow()
        user.updated_by = current_user.id
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('users.profile', user_id=user.id))

    return render_template('users/edit_profile.html',
                           title='Edit User Profile',
                           form=form,
                           user=user)


# Users - Bulk Upload Users - CSV Upload
@users_bp.route('/bulk_upload_users', methods=['GET', 'POST'])
@login_required
@admin_required
def bulk_upload_users():
    """
    This pages allows admins to bulk upload users via CSV file.
    The admin will be able to do the following:
    1. Learn how to format the CSV
    2. Select a CSV to upload

    This function will return the file and redirect to the confirm page.
    """

    if request.method == "POST":
        csv_file = request.files["csvFile"]
        if csv_file:
            filename = secure_filename(csv_file.filename)
            csv_file.save(filename)
            # Redirect to users bulk upload preview
            return redirect(url_for('users.confirm_users', filename=filename))
        else:
            flash('No file uploaded.', 'danger')

    return render_template(
        "users/users_bulk_upload.html",
        title="Users - Bulk Upload",
    )


# Users - Bulk Upload Users - CSV Upload Preview
@users_bp.route('/bulk_upload_users/confirm/<filename>',
                methods=['GET', 'POST'])
@login_required
@admin_required
def confirm_users(filename):
    """
    This page will:
    1. Verify the content of the CSV matches what's needed.
    2. Bulk create the users
    """

    # Verify file extension
    if not filename.endswith('.csv'):
        flash('Invalid file format. Please upload a CSV file.', 'danger')
        os.remove(filename)
        return redirect(url_for('users.bulk_upload_users'))

    # Parse CSV file and verify content
    users = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            if len(row) != 5:
                flash("""
Invalid CSV format. Please make sure all columns are provided.
                    """,
                      'danger'
                      )
                os.remove(filename)
                return redirect(url_for('users.bulk_upload_users'))
            users.append({
                'first_name': row[0],
                'last_name': row[1],
                'email': row[2],
                'department': row[3],
                'role': row[4]
            })

    # Create the users
    if request.method == 'POST':
        for user_data in users:
            user_data_email = user_data['email']

            # Skip if user already exists
            if User.query.filter_by(email=user_data_email).first():
                continue

            # Generate a random password
            rand_password = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=12)
            )
            # Look up department id by the department name
            department_name = user_data['department']
            department = Departments.query.filter_by(
                name=department_name).first()
            if department:
                department_id = department.id
                # Create user using the existing user creation function
                new_user = User(
                    email=user_data['email'],
                    password_hash=generate_password_hash(rand_password),
                    firstname=user_data['first_name'],
                    lastname=user_data['last_name'],
                    department_id=department_id,
                    role=user_data['role'],
                    status="active",
                    created_date=datetime.utcnow(),
                    created_by=current_user.id,
                )
                db.session.add(new_user)

                # Send email to new user
                msg = Message(
                    "KudoTrio - Forced Password Change",
                    recipients=[new_user.email],
                    sender="noreply@healthtrio.com",
                )
                msg.body = f"""
                Hello {new_user.firstname},

                You're password has been changed by an administrator.

                Your temporary password is:
                {rand_password}

                Please login and change your password.
                {url_for('users.login', _external=True)}
                """
                mail.send(msg)
            else:
                flash(
                    f"Department '{department_name}' does not exist.",
                    'danger'
                )
                os.remove(filename)
                return redirect(url_for('users.bulk_upload_users'))

        db.session.commit()
        os.remove(filename)
        flash('Users created successfully.', 'success')
        return redirect(url_for('settings.settings_users'))

    return render_template(
        "users/users_bulk_upload_confirm.html",
        title="Confirm Users",
        users=users
    )
