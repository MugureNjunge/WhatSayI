from . import main
from flask import flash, render_template, request, redirect, url_for,flash
from app.models import User, Post, Comments
from flask_login import login_required, current_user
from .forms import PostForm, CommentForm, UpdatePost
from .. import db
from ..requests import getRandom
from webbrowser import get
from ..sendMail import mail_message



@main.route('/')
def home():
    randomQuote = getRandom()

    post=Post.query.all()
    identification = post.user_id
    posted_by = User.query.filter_by(id=identification).first()
    user = User.query.filter_by(id=current_user.get_id()).first()

    recent_post = Post.query.order_by(post.id).all()

    return render_template('home.html', randomQuote=randomQuote, post=post, posted_by=posted_by, user=user, recent_post=recent_post)

@main.route('/new_post', methods=['GET','POST'])
@login_required
def post_form():
    post_form = PostForm()
    if post_form.validate_on_submit():
        text = post_form.post_text.data
        new_post = Post(text=text, user=current_user)
        new_post.save_post()

        data = User.query.all()
        for user in data:
            mail_message('New post up!', 'email/new_post', user.email, user=user)
            return redirect(url_for('main.blog'))
    return render_template('new_post.html', post_form=post_form, )


@main.route('/edit_post/<int:post_id>', methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    form = UpdatePost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated!', 'success')
        return redirect(url_for('main.blog', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content    
    return render_template('edit_post.html', form=form, title='Update Post', legend='Update Post')


@main.route('/delete_post/<int:post_id>', methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.home', post_id=post.id))


@main.route('/comments/<int:post_id>', methods=['GET','POST'])
def post_comments(post_id):
    comments = Comments.get_comments(post_id)

    post = Post.query.get(post_id)
    post_posted_by = post.user_id
    user = User.query.filter_by(id=post_posted_by).first()

    form = CommentForm()
    if form.validate_on_submit():
        comment = form.post_comment.data      
        new_comment = Comments(comment=comment, post_id=post_id, user_id=current_user.get_id())
        new_comment.save_comment()
        return redirect(url_for('main.comments',post_id = post_id))

    return render_template('comments.html', comment_form=form, comments=comments, post = post, user=user)


@main.route('/delete_comment/<int:comment_id>', methods=['GET','POST'])
@login_required
def delete_comment(comment_id):
    comment = Comments.query.filter_by(id=comment_id).first()

    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('main.blog', comment_id=comment.id))

@main.route('/all/posts')
def blog():
    posts = Post.query.all()

    return render_template('blog.html', posts=posts)    



