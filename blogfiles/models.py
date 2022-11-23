from blogfiles import db, login_manager
from datetime import datetime, timezone, timedelta
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    image = db.Column(db.String(), nullable=False, default='default.png')
    rank = db.Column(db.Integer(), nullable=False, default=0)
    posts = db.relationship('Post', backref='author', lazy=True)

def __repr__(self):
        return f'User("username": {self.username}, "email": {self.email}, "image": {self.image}'
     
class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=60), nullable=False, unique=True)
    content = db.Column(db.String(), nullable=False)
    post_date = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'Post("title": {self.title}, "content": {self.content}'
    
    
class Learn(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    desc = db.Column(db.String(length=100))
    
    
