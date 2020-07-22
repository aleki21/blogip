from . import main
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required

class addPost(FlaskForm):
    title = StringField("Post Title", validators = [Required()])
    content = TextAreaField("Your Post",validators=[Required()])
    submit = SubmitField("Add Post")

class addComment(FlaskForm):
    content = TextAreaField("Add comment", validators = [Required()])
    submit = SubmitField("Add Comment ")
    
class updatePost(FlaskForm):
    content = TextAreaField("Change post",validators=[Required()])
    submit = SubmitField("Update post")

class updateProfile(FlaskForm):
    bio = TextAreaField("Tell us about you.", validators=[Required()])
    submit = SubmitField("Submit Bio")

class mailListForm(FlaskForm):
    email = StringField("Enter email to get updates whenever new posts are made", validators= [Required()])
    submit = SubmitField("Subcribe")