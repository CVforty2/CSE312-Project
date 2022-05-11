from datetime import datetime


class Post():
    def __init__(self, sender_username, reciever_username, text, created=datetime.utcnow()):
        self.sender_username = sender_username
        self.reciever_username = reciever_username
        self.text = text
        self.created = created

    
    def __str__(self):
        return f"Sender username: {self.sender_username}, Reciever username: {self.reciever_username}, Text: {self.text}, Created: {self.created}"