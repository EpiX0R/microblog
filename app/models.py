"""
Contains Databse model classes
"""

from hashlib import md5
from datetime import datetime
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    """
    Represetns a system User
    """
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}, {}>'.format(self.username, self.email)
    
    def set_password(self, password):
        """
        Set password to generated password hash
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if password hash matches set password
        """
        current_app.logger.debug("Checking password {}".format(password))
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        """
        Follows another user
        """
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """
        Unfollows a followed user
        """
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        """
        Retrieves wheter the current user is following specified user (True) or not (False)
        """
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        """
        Returns the currents users posts combined with the followed users posts ordered by time
        """
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    @staticmethod
    @login.user_loader
    def load_user(id_):
        """
        Return user base on id.
        """
        return User.query.get(int(id_))

    def avatar(self, size="80"):
        """
        Return Gravatar URL based on email
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest() # nosec
        url = 'https://www.gravatar.com/avatar/{}?d=retro&s={}'.format(
            digest, size)
        current_app.logger.debug("Get gravatar {}".format(url))
        return url

class Post(db.Model):
    """
    Represents a User Post
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post: {}: {} By user_id {}>'.format(self.title, self.body, self.user_id)
