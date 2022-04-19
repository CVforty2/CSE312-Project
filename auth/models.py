from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))

    last_active = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, username, email, password, last_active):
        self.username = username
        self.email = email
        self.password = password
        self.last_active = last_active