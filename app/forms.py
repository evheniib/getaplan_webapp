from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app.models import Profession


class SelectProf(FlaskForm):
    select = SelectField("Professions",
        choices=[prof.name for prof in Profession.query.all()])
    submit = SubmitField("Select")
