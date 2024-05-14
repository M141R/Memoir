from flask import Blueprint, render_template, redirect, url_for, redirect, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
import os
from dotenv import load_dotenv

load_dotenv()

sendgrid_api_key = os.getenv('SENDGRID_API_KEY')

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email already exists.', category='error')
        elif username_exists:
            flash('Username already exists.', category='error')
        else:
            key = Fernet.generate_key()
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'), key=key)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!', category='success')

            s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = s.dumps(email, salt='email-confirm')

            confirm_url = url_for('auth.confirm_email', token=token, _external=True)

            message = Mail(
                from_email='mihir2726@gmail.com',
                to_emails=email,
                subject='Verify your account',
                html_content='<strong>Please click the following link to verify your account:</strong> <a href="{}">Confirm Email</a>'.format(confirm_url))
            try:
                sg = SendGridAPIClient(api_key=sendgrid_api_key)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(str(e))

    return render_template('signup.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))


@auth.route('/confirm_email/<token>', methods=['GET'])
def confirm_email(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        flash('The confirmation link is expired.')
        return redirect(url_for('index'))

    user = User.query.filter_by(email=email).first()
    if user:
        user.verified = True
        db.session.commit()

    flash('Email confirmed. Please login.', category='success')
    return redirect(url_for('auth.login'))
