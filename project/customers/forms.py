#form imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField
from wtforms.validators import DataRequired

# Flask forms (wtforms) allow you to easily create forms in format:
# variable_name = Field_type('Label that will show', validators=[V_func1(), V_func2(),...])
class AddCustomer(FlaskForm):
    name = StringField('Customer name', validators=[DataRequired()])
    age = StringField('Customer city')
    age = IntegerField('Customer age')
    submit = SubmitField('Add a customer')
