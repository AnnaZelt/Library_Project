# form imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired

# Flask forms (wtforms) allow you to easily create forms in the format:
# variable_name = Field_type('Label that will show', validators=[V_func1(), V_func2(), ...])
class CreateLoan(FlaskForm):
    customer_id = IntegerField('Customer ID', validators=[DataRequired()])
    book_id = IntegerField('Book ID', validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    return_date = DateField('Return Date', format='%Y-%m-%d')
    submit = SubmitField('Create Loan')
