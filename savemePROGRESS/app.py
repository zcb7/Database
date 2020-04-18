"""
# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userDataTest.db'
app.secret_key = "password123"

db = SQLAlchemy(app)
"""