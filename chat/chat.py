from flask import Blueprint, flash, render_template, redirect, url_for, session
from flask_login import current_user, login_required
from datetime import datetime, timedelta

from auth.models import User
from chat.models import Post
from chat.forms import ChatForm
from app import db, update_last_active


chat_bp = Blueprint("chat", __name__, template_folder="templates")


def get_active_users():
    right_now = datetime.utcnow()
    # delta = right_now - timedelta(minutes=right_now.minute - 30,
    #                       seconds=right_now.second,
    #                       microseconds=right_now.microsecond)
    # # print(f"{User.last_active} >= {delta}")
    sorted_users = list(User.query.order_by(User.last_active))

    active_users = []
    for user in sorted_users:
        # print(current_user, user)
        if current_user.is_authenticated and current_user.email != user.email:
            print(user.last_active.year, user.last_active.month, user.last_active.day, user.last_active.hour, user.last_active.minute)
            print(right_now.year, right_now.month, right_now.day, right_now.hour, right_now.minute)
            if user.last_active.year == right_now.year and user.last_active.month == right_now.month and user.last_active.day == right_now.day \
                and user.last_active.hour and right_now.hour and user.last_active.minute >= 0 and right_now.minute - 30:
                print(f"Appending {user}")
                active_users.append(user)


    print(active_users)
    return active_users


@login_required
@chat_bp.route('/', methods=['GET', 'POST'])
def index():
    update_last_active()
    online_users = get_active_users()
    print(online_users)
    return render_template('home.html', online_users=online_users)


@chat_bp.route("/dm/<username>", methods=['GET', 'POST'])
def chat(username):
    update_last_active()
    recv = User.query.filter_by(username=username).first()
    # print(current_user.id, recv.id)

    posts_sender = Post.query.filter_by(sender_id=current_user.id).filter_by(reciever_id=recv.id).all()
    posts_recv = Post.query.filter_by(sender_id=recv.id).filter_by(reciever_id=current_user.id).all()

    posts = posts_sender + posts_recv
    posts.sort(key=lambda x: x.created)


    form = ChatForm()

    if form.validate_on_submit():
        
        p = Post(current_user.id, recv.id, form.text.data, datetime.utcnow())
        db.session.add(p)
        db.session.commit()

        flash("Sent message!", 'success')
        
        return redirect(url_for('chat.chat', username=username))

    return render_template("dm.html", form=form, posts=posts, username=recv.username)


@chat_bp.route('/test', methods=['GET', 'POST'])
def test():
    form = ChatForm()

    if form.validate_on_submit():
        p = Post(1, 1, form.text.data, datetime.utcnow())
        db.session.add(p)
        db.session.commit()

        return redirect(url_for('chat.test'))

    return render_template("test.html", form=form)
    


