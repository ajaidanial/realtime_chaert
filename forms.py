from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class DefectForm(FlaskForm):
    """Form for defect table."""

    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Save")


class VehicleForm(FlaskForm):
    """Form for vehicle table."""

    value = IntegerField("Value", validators=[DataRequired()])
    defect = IntegerField("Defect", validators=[DataRequired()])
    submit = SubmitField("Save")
