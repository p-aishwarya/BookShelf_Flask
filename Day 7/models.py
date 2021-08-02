from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'Users'
    email = db.Column(db.String,nullable=False,primary_key=True)
    pwd = db.Column(db.String,nullable=False)
    repeat = db.Column(db.String,nullable=False)

class Bookdetails(db.Model):
    __tablename__= 'Bookdetails'
    id = db.Column(db.String,primary_key=True)
    title = db.Column(db.String,nullable=False)
    author = db.Column(db.String,nullable=False)
    year = db.Column(db.String,nullable=False)