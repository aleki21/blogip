from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    '''
    Class to define Users
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String)
    fullname = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    bio = db.Column(db.String)
    profile_pic_url = db.Column(db.String)
    pass_secure = db.Column(db.String)
    posts = db.relationship("Post", backref = 'user', lazy = 'dynamic')

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User{self.username}'

# Class for posts
class Post(db.Model):
    '''
    Class to define Users
    '''
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    image_url = db.Column(db.String)
    content = db.Column(db.String)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,  db.ForeignKey('users.id'))
    comments = db.relationship("Comment", backref='post', lazy ='dynamic')

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_user_post(cls,id):
        user_posts = Post.query.filter_by(user_id = id).all()
        return user_posts

    def __repr__(self):
        return f"Post {self.title}"

#class for comments
class Comment(db.Model):
    '''
    Class to define Comments
    '''
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String)
    date =db.Column(db.DateTime,default = datetime.utcnow())
    post_id = db.Column(db.Integer, db. ForeignKey('posts.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(post_id = id).all()
        return comments

class MailList(db.Model):
    __tablename__ = "maillist"
    
    id = db.Column(db.Integer,primary_key =True)
    email = db.Column(db.String) 

    def save_mail(self):
        db.session.add(self)
        db.session.commit()