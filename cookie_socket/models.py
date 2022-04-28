from app import db


class CookieClick(db.Model):
    __tablename__ = 'cookie'

    id = db.Column(db.Integer, primary_key=True)
    click = db.Column(db.Integer, nullable=False)

    def __init__(self, click):
        self.click = click