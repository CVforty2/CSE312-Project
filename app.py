from flask import Flask
from flask_login import LoginManager
from flask_login import current_user
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cse312'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://qesbcvenrwjudb:355d5721bb2ee7a8c12ac387235ae3b8ae8f5f95c6554f99f73731f6cd45bcb4@ec2-3-225-79-57.compute-1.amazonaws.com:5432/deefogb5ult2oi"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy DB
db = SQLAlchemy(app)

# from auth.models import User
# from chat.models import Post
# from cookie_socket.models import CookieClick




# Helper to see last active members
# Time out period is specified else where
# @app.before_request
def update_last_active():
    current_user.last_active = datetime.utcnow()
    print(current_user.last_active)
    db.session.commit()


def init_app():
    # Initialize Blueprints

    from auth.auth import auth_bp
    from chat.chat import chat_bp
    from cookie_socket.cookie_sock import sock_bp

    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(chat_bp, url_prefix="/")
    app.register_blueprint(sock_bp, url_prefix="/")

    from chat.models import Post
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
