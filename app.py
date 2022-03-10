from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cse312'

mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]

# Add collections for users, posts, multimedia data
user_collections = db["users"]


def init_app():
    # Initialize Blueprints

    from auth.auth import auth
    from chat.chat import chat

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(chat, url_prefix="/")

    # login_manager = LoginManager()
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     # update with pymongo
    #     pass




if __name__ == "__main__":
    init_app()
    app.run(debug=True, host='0.0.0.0', port=8080)
