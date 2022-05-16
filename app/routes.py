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