from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Post, User
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/index')
def index():
    return render_template('index.html', user=current_user, posts=posts)

@views.route('/profile')
def profile():
    return render_template('profile.html')

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        title = request.form.get('title')

        if not text:
            flash('Post cannot be empty', category='error')
        elif not title:
            flash('Title cannot be empty', category='error')    
        else:
            post = Post(text=text,title=title, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.index'))

    return render_template('createpost.html', user=current_user)

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exisr", category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')
        
    return redirect(url_for('views.index'))

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists', category='error')
        return redirect(url_for('views.index'))
    
    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)

@views.route('/post/<id>')
@login_required
def post_detail(id):
    post = Post.query.get(id)
    return render_template('post_page.html', post=post,user=current_user)
