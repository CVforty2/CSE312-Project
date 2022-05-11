from flask import Blueprint, flash, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import user_collection
from auth.forms import RegistrationForm, LoginForm
from auth.models import User
from chat.models import Post


auth_bp = Blueprint("auth", __name__, template_folder="templates")

def flash_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"ERROR --> {field}: {error}", 'fail')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(form.username.data, form.email.data, hashed_password)

        user_collection.insert_one(new_user.__dict__)

        flash("User created successfully!", 'success')

        return redirect(url_for('auth.login'))

    flash_form_errors(form)
    return render_template("register.html", form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = user = list(user_collection.find({"email": form.email.data}))
        print(user)

        if len(user) > 0:
            user = user[0]
            if check_password_hash(user['password'], form.password.data):
                del user['_id']
                session['current_user'] = user
                flash("Log in successfully", 'success')
                return redirect(url_for("chat.index"))
            else:
                flash("No user found by that email address", 'fail')

    flash_form_errors(form)
    return render_template("login.html", form=form)


@auth_bp.route('/logout')
def logout():
    session.pop("current_user", None)
    flash("User logged out!", 'success')
    return redirect(url_for("chat.index"))
