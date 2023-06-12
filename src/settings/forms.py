"""
Settings - Forms
This file contains the forms for the settings blueprint.
"""

# Imports
from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField
)
from wtforms.validators import DataRequired


# Form - Add and Edit Department
class DepartmentForm(FlaskForm):
    """
    Form for users to add departments
    """

    name = StringField("Name", validators=[DataRequired()],
                       render_kw={"class": "form-control"})
    submit = SubmitField("Save",
                         render_kw={"class": "btn btn-primary"})
