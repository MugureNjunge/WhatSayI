import os
from flask import render_template, url_for, flash, redirect, abort,request
from app import app, db
from app.forms import SignupForm, LoginForm, PostForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from app.requests import get_quotes

@app.route("/")
def home():

    posts = Post.query.all()
    return render_template("home.html", posts=posts)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():

        user = User(username=form.username.data,
                    email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Account created!You can now log in!', 'success')
        return redirect(url_for('login'))
    return render_template("signup.html", title='Signup', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password = User.query.filter_by(password=form.password.data).first()

        if user and password:
            login_user(user, remember=form.remember.data)
            flash('Login successful', 'success')
            return redirect(url_for('home'))

        else:
            flash('Login unsuccessful.Please check your email and password', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))   

@app.route("/profile")
@login_required
def profile():
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
    return render_template("profile.html", title='Profile', image_file=image_file)


@app.route("/blog/new", methods=['GET', 'POST'])
@login_required
def newblog():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your blog has been created!', 'success')
        return redirect(url_for('home'))
    return render_template("newblog.html", title='New Blog', 
    form=form, legend='New Post')    

@app.route("/post/<int:post_id>")
def post(post_id):
    post = post.query.get_or_404(post_id)
    return render_template('blog.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post successfully updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':    
        form.title.data = post.title
        form.content.data = post.content
    return render_template("newblog.html", title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
