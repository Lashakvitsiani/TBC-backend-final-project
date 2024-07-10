from ext import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())
    img = db.Column(db.String())
    link = db.Column(db.String())
    weblink = db.Column(db.String())
    likes = db.Column(db.Integer, default=1)

    def __init__(self, name, img, price, link, weblink):
        self.name = name
        self.img = img
        self.price = price
        self.link = link
        self.weblink = weblink


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.String(), default="user")

    def __init__(self, username, email, password, role="Guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'), nullable=False)

    db.UniqueConstraint('user_id', 'product_id', name='unique_user_product_like')
    user = db.relationship('User', backref=db.backref('likes', lazy='dynamic'))
    product = db.relationship('Product', backref=db.backref('likes_by_users', lazy='dynamic'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
