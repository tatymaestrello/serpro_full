from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app
from sqlalchemy.dialects.sqlite import (BLOB)

db = SQLAlchemy(app)

class Register(db.Model):
    __tablename__ = "register"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(200))
    company = db.Column('company', db.String(200))
    options = db.Column('options', db.String(200))
    workload = db.Column('workload', db.Boolean, default=False)
    complete = db.Column('complete', db.Boolean, default=False)
    errors = db.Column('error', db.String(500))
    creation_date = db.Column('creation_date', db.DateTime, default=datetime.utcnow)

class Workload(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    filename = db.Column('filename', db.String(200))
    payload = db.Column('payload', BLOB)
    mimetype = db.Column('mimetype', db.String(100))