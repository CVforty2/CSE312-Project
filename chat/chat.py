from flask import Blueprint, flash, render_template, redirect, url_for
# Import chat collections or however we decide to store it

chat = Blueprint("chat", __name__, template_folder="templates")


@chat.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


@chat.route('/create', methods=['GET', 'POST'])
def create_post():
    pass


def edit_post():
    pass


def delete_post():
    pass


def react_to_post():
    pass