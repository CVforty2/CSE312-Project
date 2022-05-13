from flask import Blueprint, flash, render_template, redirect, url_for, session, send_from_directory
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import time

from auth.models import User
from chat.models import Post
from chat.forms import ChatForm
from app import user_collection, msg_collection


chat_bp = Blueprint("chat", __name__, template_folder="templates")

UPLOAD_FOLDER = "chat/user_images"


@chat_bp.route("/uploads/<filename>")
def send_uploaded_file(filename=''):
    return send_from_directory(
        UPLOAD_FOLDER, filename
    )



def activate_user():
    if 'current_user' in session:
        username = session['current_user']['username']
        user_collection.update_one({'username': username}, {'$set': {'last_active': datetime.utcnow()}})



def get_active_users():
    right_now = datetime.utcnow()
    users = list(user_collection.find({}))

    active_users = []
    for user in users:
        # print(current_user, user)
        if 'current_user' in session and session['current_user']['email'] != user['email']:
            print(user['last_active'].year, user['last_active'].month, user['last_active'].day, user['last_active'].hour, user['last_active'].minute)
            print(right_now.year, right_now.month, right_now.day, right_now.hour, right_now.minute)
            if user['last_active'].year == right_now.year and user['last_active'].month == right_now.month and user['last_active'].day == right_now.day \
                and user['last_active'].hour and right_now.hour and user['last_active'].minute >= 0 and right_now.minute - 30:
                print(f"Appending {user}")
                active_users.append(user)

    print(active_users)
    return active_users


@chat_bp.route('/', methods=['GET', 'POST'])
def index():
    # Update online users
    activate_user()
    online_users = get_active_users()
    print(online_users)
    return render_template('home.html', online_users=online_users)


@chat_bp.route("/dm/<username>", methods=['GET', 'POST'])
def chat(username):
    if 'current_user' not in session:
        return redirect(url_for('auth.login'))
        
    activate_user()

    out_msgs = list(msg_collection.find({'sender_username': session['current_user']['username'], 'reciever_username': username}))
    in_msgs = list(msg_collection.find({'sender_username': username, 'reciever_username': session['current_user']['username']}))

    posts = out_msgs + in_msgs
    posts.sort(key=lambda x: x['created'])


    form = ChatForm()

    if form.validate_on_submit():

        image_name = ""
        if form.picture.data != None:
            image_name = secure_filename(str(time.time())+ '_' + form.picture.data.filename)
            form.picture.data.save(os.path.join(UPLOAD_FOLDER, image_name))
        
        p = Post(session['current_user']['username'], username, form.text.data, image_name, datetime.utcnow())
        msg_collection.insert_one(p.__dict__)

        flash("Sent message!", 'success')
        
        return redirect(url_for('chat.chat', username=username))

    return render_template("dm.html", form=form, posts=posts, username=username)






def msg_data(user1, user2):
    out_msgs = list(msg_collection.find({'sender_username': user1, 'reciever_username': user2}))
    in_msgs = list(msg_collection.find({'sender_username': user2, 'reciever_username': user1}))

    posts = out_msgs + in_msgs
    posts.sort(key=lambda x: x['created'])

    count = 0
    for i in range(len(posts)-1, 0, -1):
        if posts[i]['sender_username'] == user1:
            break
        count += 1

    return count
    

@chat_bp.route('/testing')
def get_unread_posts():
    active_users = get_active_users()

    unread_posts = {}
    for user in active_users:
        unread_posts[user['username']] = msg_data(session['current_user']['username'], user['username'])
    
    print(unread_posts)
    return unread_posts
