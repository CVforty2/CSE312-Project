from app import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reciever_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.String(2000))

    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, sender_id, reciever_id, text, created=datetime.utcnow()):
        self.sender_id = sender_id
        self.reciever_id = reciever_id
        self.text = text
        self.created = created