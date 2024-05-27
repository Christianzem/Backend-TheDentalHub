from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, ValidationError 

class PatientForm(FlaskForm):
    first_name = StringField("First Name",validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    birth_date = DateField("Date of Birth", validators=[DataRequired()], format='%Y-%m-%d' )
    patient_number = StringField("Patient Number", validators=[DataRequired()])

