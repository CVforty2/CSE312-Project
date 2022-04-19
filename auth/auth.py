from flask import Blueprint, flash, render_template, redirect, url_for
from app import user_collections
#from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    pass


@auth.route('/login', methods=['GET', 'POST'])
def login():
    pass


@auth.route('/logout')
def logout():
    pass


@auth.route('/profile/<username>')
def get_profile(username):
    pass