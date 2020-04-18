from flask_table import Table, Col, LinkCol

class Results(Table):
    """user_id = Col('UserId')"""
    username = Col('UserName')
    password = Col('Password')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='user_id'))
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='user_id'))