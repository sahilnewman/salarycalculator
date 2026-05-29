from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))

    mobile = db.Column(db.String(20))
    age = db.Column(db.Integer)

    gender = db.Column(db.String(20))
    education = db.Column(db.String(100))

    email = db.Column(db.String(150), unique=True)

    username = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(255))