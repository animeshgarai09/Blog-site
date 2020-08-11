from project import db,loginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@loginManager.user_loader
def loader(userId):
    return user.query.get(userId)


class user(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    fullname = db.Column(db.String(64), unique=True, index=True)
    hashPassword = db.Column(db.String(128),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)

    posts = db.relationship('blogPost', backref='author', lazy=True)

    def __init__(self,email,fullname,password):
        self.email=email
        self.fullname=fullname
        self.hashPassword=generate_password_hash(password)
    
    def checkPassword(self,password):
        return check_password_hash(self.hashPassword,password)

    def __repr__(self):
        return f'Full name:   {self.fullname}'



class blogPost(db.Model):
    users=db.relationship(user)

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    blog_image = db.Column(db.String(20), nullable=False, default='default_blog_image.jpg')
    title=db.Column(db.String(100),nullable=False)
    short=db.Column(db.String(140),nullable=False)
    description=db.Column(db.Text,nullable=False)

    def __init__(self,title,description,user_id,blog_image,short):
        self.title=title
        self.description=description
        self.user_id=user_id
        self.blog_image=blog_image
        self.short=short

    def __repr__(self):
        return f'Blog post: {self.id} --- Date: {self.date} --- Title:  {self.title}'