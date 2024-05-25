from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired

class DentalProsthesis(FlaskForm):
    prosthesis_type = SelectField('Prosthesis Type', choices=[('Crown','Crown'), ('Denture','Denture'), ('Partial','Partial'), ('Night Guard','Night Guard')], validators=[DataRequired()])
    checkbox = BooleanField('Checkbox')
    selected_date = DateField('Selected Date', format='%Y-%m-%d')
    submit = SubmitField('Add Dental Prosthesis')