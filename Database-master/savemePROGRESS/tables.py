from flask_table import Table, Col, LinkCol

class Results(Table):
    #user_id = Col('UserId')
    username = Col('UserName')
    highScore = Col('HighScore')
