from flask import Flask, g
from flask_login import LoginManager
from flask_login import current_user
from datetime import datetime
from pymongo import MongoClient
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cse312'

mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]

user_collection = db["user"]
msg_collection = db["msg"]
click_collection = db["click"]



def init_app():
    # Initialize Blueprints

    from auth.auth import auth_bp
    from chat.chat import chat_bp

    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(chat_bp, url_prefix="/")



if __name__ == "__main__":
    init_app()
    app.run(debug=True, host='0.0.0.0', port=8080)
