# forms.py

from wtforms import Form, StringField, SelectField, validators

class SearchForm(Form):

    choices = [('User_id', 'User_id'),
               ('Username', 'Username')]
    select = SelectField('Search by:', choices=choices) 
    search = StringField('')


class EditForm(Form):

    username = StringField('Username')
    password = StringField('Password')
