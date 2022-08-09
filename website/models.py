from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.String(150),unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    address = db.Column(db.String(250))
    checking = db.relationship('Checking')
    savings = db.relationship('Savings')
    stock = db.relationship('Stock')

class Checking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)
    overdraft = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Savings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)
    interest = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    opened = db.Column(db.Date())
    last = db.Column(db.Date())
    interest_earned = db.Column(db.Float)



class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(150),unique=True)
    price_bought = db.Column(db.Float(150))
    price_current = db.Column(db.Float(150))
    shares = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String(400))
    name = db.Column(db.String(200))


   





    
