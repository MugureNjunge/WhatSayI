from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField ,SubmitField
from wtforms.validators import DataRequired
from flask_login import current_user



class UpdatePost(FlaskForm):
    text = TextAreaField('Edit post here',validators = [DataRequired()])
    submit = SubmitField('Update')


class PostForm(FlaskForm):
    post_text = TextAreaField('Your post here', validators=[DataRequired()]) 
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    post_comment = TextAreaField('Make a comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

