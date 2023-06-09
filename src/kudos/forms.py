"""
Kudos - Forms
This file contains the forms for the kudos blueprint.
"""

# Imports
from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField, StringField, SelectField, SubmitField
)
from wtforms.validators import DataRequired


# Form - Add and Edit Kudo
class KudoForm(FlaskForm):
    """
    Form for users to add and edit kudos
    """

    receiving_user_id = SelectField(
        "To",
        coerce=int,
        validators=[DataRequired()],
        render_kw={"class": "form-control select2"}
        )
    kudo_message = TextAreaField("Kudo Message", validators=[DataRequired()],
                                 render_kw={"class": "form-control",
                                            "rows": 5})
    meme_top_text = StringField("Text Top",
                                render_kw={"class": "form-control"})
    meme_bottom_text = StringField("Text Bottom",
                                   render_kw={"class": "form-control"})
    meme_template = SelectField("Meme Template", coerce=str,
                                render_kw={"class": "form-control"})
    submit = SubmitField("Save",
                         render_kw={"class": "btn btn-primary"})
    cancel = SubmitField('Cancel',
                         render_kw={'formnovalidate': True,
                                    "class": "btn btn-outline-primary"})
