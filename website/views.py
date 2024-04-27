from flask import Blueprint, render_template
from flask_login import current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/index')
def index():
    return render_template('index.html', user=current_user)

@views.route('/profile')
def profile():
    return render_template('profile.html')