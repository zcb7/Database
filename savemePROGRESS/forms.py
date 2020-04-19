# forms.py
from flask_wtf import Form
from wtforms import StringField, TextField, PasswordField, SelectField, validators
from wtforms.validators import DataRequired

class SearchForm(Form):

    choices = [('Blue', 'Blue'),
               ('Red', 'Red'),
               ('All', 'All')]
    select = SelectField('Search for:', choices=choices) 
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

class NewUserForm(Form):

    choices = [('Blue', 'Blue'),
               ('Red', 'Red')]
    select = SelectField('Select Team:', choices=choices)
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class DeleteForm(Form):

    username = StringField('Username', validators=[DataRequired()])
    #password = StringField('Password') # validators=[DataRequired()])
