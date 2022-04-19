from flask import Flask
from flask_login import LoginManager
from flask_login import current_user
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cse312'
app.config['SQLALCHEMY_DATABASE_URI'] = TEST
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy DB
db = SQLAlchemy(app)

# Helper to see last active members
# Time out period is specified else where
@app.before_request
def update_last_active():
    current_user.last_active = datetime.utcnow()
    db.session.commit()


def init_app():
    # Initialize Blueprints

    from auth.auth import auth
    from chat.chat import chat

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(chat, url_prefix="/")

    from auth.models import User
    init_db(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
       return User.query.get(int(id))


def init_db(app):
    if not os.path.exists("website/" + 'db.sqlite'):
        db.create_all(app=app)
        print("Created database!")




if __name__ == "__main__":
    init_app()
    app.run(debug=True, host='0.0.0.0', port=8080)
