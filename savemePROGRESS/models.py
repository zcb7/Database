from app import db

class Userdata(db.Model):

    __tablename__ = "userdata"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)



