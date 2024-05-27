from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired

class DentalProsthesis(FlaskForm):
    prosthesis_type = SelectField('Prosthesis Type', choices=[('Crown','Crown'), ('Denture','Denture'), ('Partial','Partial'), ('Night Guard','Night Guard')], validators=[DataRequired()])
    checkbox1 = BooleanField('Checkbox')
    checkbox2 = BooleanField('Checkbox')
    checkbox3 = BooleanField('Checkbox')
    checkbox4 = BooleanField('Checkbox')
    selected_date1 = DateField('Selected Date', format='%Y-%m-%d')
    selected_date2 = DateField('Selected Date', format='%Y-%m-%d')
    selected_date3 = DateField('Selected Date', format='%Y-%m-%d')
    selected_date4 = DateField('Selected Date', format='%Y-%m-%d')
    submit = SubmitField('Add Dental Prosthesis')