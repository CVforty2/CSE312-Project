from flask import Blueprint, flash, render_template, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import db
from auth.forms import RegistrationForm, LoginForm, ChatForm
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

        db.session.add(new_user)
        db.session.commit()

        flash("User created successfully!", 'success')

        return redirect(url_for('auth.login'))

    flash_form_errors(form)
    return render_template("register.html", form=form)



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                db.session.add(user)
                db.session.commit()
                flash("Log in successfully", 'success')
                return redirect(url_for("chat.index"))
            else:
                flash("No user found by that email address", 'fail')

    flash_form_errors(form)
    return render_template("login.html", form=form)





@auth_bp.route('/logout')
def logout():
    logout_user()
    flash("User logged out!", 'success')
    return redirect(url_for("home.index"))



@auth_bp.route('/profile/<username>')
def get_profile(username):
    user = User.query.filter_by(username=username)
    posts = Post.query.filter(Post.sender_id.like==current_user.id). \
        filter(Post.sender_id.like==user.id)

    form = ChatForm()
    if form.validate_on_submit():
        post = Post(current_user.id, user.id, form.text.data)
        db.session.add(post)
        db.session.commit()

    return render_template("profile.html", username=user, posts=posts)