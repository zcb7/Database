# forms.py
from flask_wtf import Form
from wtforms import StringField, TextField, PasswordField, SelectField, validators
from wtforms.validators import DataRequired

class SearchForm(Form):

    choices = [('User_id', 'User_id'),
               ('Username', 'Username')]
    select = SelectField('Search by:', choices=choices) 
    search = StringField('')

class EditForm(Form):

    username = StringField('Username') # validators=[DataRequired()])
    password = StringField('Password') # validators=[DataRequired()])

class LoginForm(Form):
    """Form class for user login."""
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class PasswordForm(Form):

    password = PasswordField('New Password', validators=[DataRequired()])
