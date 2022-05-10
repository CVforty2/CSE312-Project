from flask import Blueprint, flash, render_template, redirect, url_for, session, Flask, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_sock import Sock
import hashlib
import base64
import random


from app import db
import app
from cookie_socket.models import CookieClick
import json

sock_bp = Blueprint("sock", __name__, template_folder="templates")
sock = Sock(Flask(__name__))
wsusers = []
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

#just do image hosting, user sends an image which is sent out to all other users and displayed to them along with their name

@sock_bp.route("/websocket", methods=['GET'])
def wsFunc():
    headers = request.data.decode().split("\r\n")
    swk = ""
    for header in headers:
        if "Sec-WebSocket-Key" in header:
            swk = header.replace("Sec-WebSocket-Key: ", "")
    hash = hashlib.sha1((swk + GUID).encode())
    enc = base64.b64encode(hash.digest())
    userID = {"username": randUserID()} #replace this with the actual user's username
    print("handshake complete")
    return (("HTTP/1.1 101 Switching Protocols\r\nConnection: Upgrade\r\nUpgrade: websocket\r\nSec-WebSocket-Accept: ").encode() + enc + ("\r\n\r\n").encode())
    while True:
        print("entering loop")
        request.data()
        print("received second message")
        responding = {"messageType": "chatMessage", "message": "server is responding"}
        return responding


def randUserID():
    dig1 = random.randint(0,9)
    dig2 = random.randint(0, 9)
    dig3 = random.randint(1, 9)
    ID = dig1 + dig2 * 10 + dig3 * 100
    userID = "User" + str(ID)
    return(userID)


@sock_bp.route("/cookieclicker", methods=['GET', 'POST'])
def clickerPage():
    return render_template('cookie.html')

@sock_bp.route("/functions.js", methods=["GET"])
def jsFunc():
    js = open("../static/functions.js", 'r', encoding="utf-8").read()
    return js

@sock_bp.route("/image/cookie.jpg", methods=["GET"])
def cookieImg():
    cookie = open("../static/cookie.jpg", 'rb').read()
    return cookie


@sock_bp.route("/cookiecount", methods=['GET'])
def clickerCount():
    single_entry = CookieClick.query.all()[0]
    return single_entry