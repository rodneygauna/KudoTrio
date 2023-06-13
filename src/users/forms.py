"""
User - Forms
This file contains the forms for the users blueprint.
"""

# Imports
from flask_wtf import FlaskForm
from wtforms import (
    StringField, EmailField, PasswordField, SubmitField, SelectField
)
from wtforms.validators import DataRequired, Email, EqualTo
from src.dictionaries.dictionaries import (
    USER_ROLE_CHOICES, STATUS_CHOICES
)


# Form - Login
class LoginForm(FlaskForm):
    """
    Form for users to login
    """

    email = EmailField("Email", validators=[DataRequired(), Email()],
                       render_kw={"class": "form-control"})
    password = PasswordField("Password", validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    submit = SubmitField("Login",
                         render_kw={"class": "btn btn-primary"})


class UserRegistrationForm(FlaskForm):
    """
    Form for users to register
    """

    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"class": "form-control"})
    firstname = StringField('First Name', validators=[DataRequired()],
                            render_kw={"class": "form-control"})
    lastname = StringField('Last Name', validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    department = SelectField('Department', coerce=int,
                             validators=[DataRequired()],
                             render_kw={"class": "form-control select2"})
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         EqualTo(
                                             'confirm_password',
                                             message='Passwords must match.')],
                             render_kw={"class": "form-control"})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')],
                                     render_kw={"class": "form-control"})
    submit = SubmitField('Save',
                         render_kw={"class": "btn btn-primary"})


# Form - Add and Edit User
class UserForm(FlaskForm):
    """
    Form for users to add and edit users
    """

    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"class": "form-control"})
    firstname = StringField('First Name', validators=[DataRequired()],
                            render_kw={"class": "form-control"})
    lastname = StringField('Last Name', validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    department = SelectField('Department', coerce=int,
                             validators=[DataRequired()],
                             render_kw={"class": "form-control select2"})
    role = SelectField('Role', choices=USER_ROLE_CHOICES,
                       default=USER_ROLE_CHOICES[1][0],
                       validators=[DataRequired()],
                       render_kw={"class": "form-control"})
    submit = SubmitField('Save',
                         render_kw={"class": "btn btn-primary"})


# Form - Change Password
class ChangePasswordForm(FlaskForm):
    """
    Form for users to change their password
    """

    password = PasswordField(
        'Password',
        validators=[DataRequired(),
                    EqualTo('confirm_password',
                            message='Passwords must match.')],
        render_kw={"class": "form-control"}
        )
    confirm_password = PasswordField('Confirm Password',
                                     render_kw={"class": "form-control"})
    submit = SubmitField('Save',
                         render_kw={"class": "btn btn-primary"})


# Form - Change User Status
class ChangeUserStatusForm(FlaskForm):
    """
    Form for users to change the status of a user
    """

    status = SelectField('Status', choices=STATUS_CHOICES,
                         validators=[DataRequired()],
                         render_kw={"class": "form-control"})
    submit = SubmitField('Save',
                         render_kw={"class": "btn btn-primary"})
