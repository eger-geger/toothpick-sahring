from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    toothpick_id = db.Column(db.Integer, db.ForeignKey('toothpick.id'), nullable=False)
    since = db.Column(db.DateTime, server_default=text("(DATETIME('now'))"))
    user = db.relationship('User')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=text("(DATETIME('now'))"))

class Toothpick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=text("(DATETIME('now'))"))
    owners = db.relationship('Owner', order_by=Owner.since.desc(), lazy='joined')