from datetime import datetime

class User():
    def __init__(self, username, email, password, last_active=datetime.utcnow()):
        self.username = username
        self.email = email
        self.password = password
        self.last_active = last_active

    
    def __str__(self):
        return f"Username: {self.username}, Email: {self.email}, Password: {self.password}, Last Active: {self.last_active}"