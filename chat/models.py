from app import db

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reciever_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.String(2000))

    def __init__(self, sender_id, reciever_id, text):
        self.sender_id = sender_id
        self.reciever_id = reciever_id
        self.text = text