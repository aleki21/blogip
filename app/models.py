from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(255))

        @property
        def password(self):
            raise AttributeError('You cannot read the password attribute')

        @password.setter
        def password(self, password):
            self.pass_secure = generate_password_hash(password)


        def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'

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
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    comment_content = db.Column(db.String())
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_comment(self):
            db.session.add(self)
            db.session.commit()

    @classmethod
    def get_comments(cls,id):
            comments = Comment.query.filter_by(pitch_id=id).all()
            return comments
                
    def __repr__(self):
        return f'COMMENT {self.comment_content}'
