from flask import render_template, url_for, flash, redirect
from app import app, db
from app.forms import SignupForm, LoginForm, PostForm,CommentForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


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


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(category=form.category.data, title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your blog has been created!', 'success')
        return redirect(url_for('home'))
    return render_template("create_post.html", title='New Blog', form=form)

@app.route('/comment/<int:blog_id>',methods = ['GET','POST'])
@login_required
def comment(post_id):
    post=post.query.get_or_404(post_id)
    form = CommentForm()
    allComments = comment.query.filter_by(post_id = post_id).all()
    if form.validate_on_submit():
        postedComment = comment(comment=form.comment.data,user_id = current_user.id, post_id = post_id)
        post_id = post_id
        db.session.add(postedComment)
        db.session.commit()
        flash('Your comment is posted')
        
        return redirect(url_for('comment',post_id=post_id))

    return render_template("comment.html",post=post, title='Add a comment!', form = form,allComments=allComments)    
