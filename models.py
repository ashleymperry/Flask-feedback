from flask_sqlalchemy import SQLAlchemy
import bcrypt
import pdb

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "users"

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        encoded = pwd.encode('utf-8')
        hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        u = User.query.filter_by(username=username).first()
        if u and bcrypt.checkpw(pwd.encode('utf-8'), u.password.encode('utf-8')):
            return u
        else:
            return False

    username = db.Column(db.String(20), nullable=False, primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    feedback = db.relationship('Feedback', backref='user', cascade='all, delete-orphan')

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'))