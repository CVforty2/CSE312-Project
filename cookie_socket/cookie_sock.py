from flask import Blueprint, flash, render_template, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user

# Import flask sock

from app import db
from cookie_socket.models import CookieClick

sock_bp = Blueprint("sock", __name__, template_folder="templates")


@sock_bp.route('/cookie-click', methods=['GET', 'POST'])
def cookie_click():
    # update single cookie click number
    single_entry = CookieClick.query.all()[0]
    single_entry.click += 1
    db.session.commit()
    return render_template('cookie.html')