from flask import Blueprint, flash, render_template, redirect, url_for, session
from datetime import datetime, timedelta

from auth.models import User

chat = Blueprint("chat", __name__, template_folder="templates")


def get_active_users():
    right_now = datetime.utcnow()
    delta = right_now - timedelta(minutes=right_now.minute - 30,
                          seconds=right_now.second,
                          microseconds=right_now.microsecond)

    active_users = User.query.filter(User.last_active >= delta)
    return active_users


@chat.route('/', methods=['GET', 'POST'])
def index():
    online_users = get_active_users()
    return render_template('home.html', online_users=online_users)


@chat.route("/dm/<username>", methods=['GET', 'POST'])
def chat(username):
    pass


@chat.route('/create', methods=['GET', 'POST'])
def create_post():
    pass


def edit_post():
    pass


def delete_post():
    pass


def react_to_post():
    pass

