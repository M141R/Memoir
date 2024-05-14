from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
import requests
from flask_login import current_user, login_required
from .models import Post, User, Category
from . import db
from datetime import datetime, timedelta
import calendar
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

tinymce_api_key = os.getenv('TINYMCE_API_KEY')



views = Blueprint('views', __name__)

@views.route('/')
@views.route('/index')
def index():
    return render_template('index.html', user=current_user)

@views.route('/profile')
def profile():
    return render_template('profile.html')

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        title = request.form.get('title')
        category_id = request.form.get('category')
        new_category_name = request.form.get('new_category')

        if not text:
            flash('Post cannot be empty', category='error')
        elif not title:
            flash('Title cannot be empty', category='error')    
        else:
            cipher_suite = Fernet(current_user.key) 
            cipher_text = cipher_suite.encrypt(text.encode())  
            if new_category_name:
                category = Category(name=new_category_name)
                db.session.add(category)
                db.session.commit()
            else:
                category = Category.query.get(category_id)

            post = Post(text=cipher_text, title=title, author=current_user.id, category=category)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.index'))
        
    categories = Category.query.all()
    return render_template('createpost.html', user=current_user,categories=categories,tinymce_api_key=tinymce_api_key)

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exisr", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')
        
    return redirect(url_for('views.index'))

@views.route("/posts/<username>", defaults={'year': None, 'month': None, 'day': None})
@views.route("/posts/<username>/<int:year>/<int:month>/<int:day>")
@login_required
def posts(username, year, month, day):
    user = User.query.filter_by(username=username).first()
    now = datetime.now()

    if not user:
        flash('No user with that username exists', category='error')
        return redirect(url_for('views.index'))

    # if not user.email_confirmed:
    #     flash('You must confirm your email to view posts', category='error')
    #     return redirect(url_for('views.index'))
    
    if year and month and day:
        date = datetime(year, month, day)
        next_day = date + timedelta(days=1)
        posts = Post.query.filter(Post.date_created >= date, Post.date_created < next_day, Post.author == user.id).all()
    else:
        posts = Post.query.filter_by(author=user.id).all()

    if not year or not month:

        year = now.year
        month = now.month
        
    post_dates = [post.date_created.date() for post in Post.query.filter_by(author=current_user.id).all()]
    return render_template("posts.html", user=current_user, posts=posts, username=username, year=now.year, month=now.month, calendar=calendar, post_dates=post_dates, datetime=datetime)

@views.route('/post/<id>')
@login_required
def post_detail(id):
    post = Post.query.filter_by(id=id).first()
    cipher_suite = Fernet(current_user.key)
    plain_text = cipher_suite.decrypt(post.text).decode()
    return render_template('post_page.html',post=post, plain_text=plain_text,user=current_user)






