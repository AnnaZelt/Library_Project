#form imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField
from wtforms.validators import DataRequired

# Flask forms (wtforms) allow you to easily create forms in format:
# variable_name = Field_type('Label that will show', validators=[V_func1(), V_func2(),...])
class CreateBook(FlaskForm):
    name = StringField('Book name', validators=[DataRequired()])
    author = StringField('Author name')
    year_published = IntegerField('Publishing year')
    type = IntegerField('Loan period')
    submit = SubmitField('Create club')
