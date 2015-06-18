from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  create_time = db.Column(db.DateTime)
  email = db.Column(db.String, unique=True)
  uuid = db.Column(db.String, unique=True)
  verified = db.Column(db.Boolean, default=False)
  wants_emails = db.Column(db.Boolean, default=True)
  wishlist_items = db.relationship('WishlistItem', backref='user', lazy='dynamic')

  def to_json(self):
    return {
      "email": self.email,
      "uuid": self.uuid,
      "verified": self.verified,
    }

  def from_json(self, source):
    if 'email' in source:
      self.email = source['email']
    if 'uuid' in source:
      self.uuid = source['uuid']
    if 'verified' in source:
      self.verified = source['verified']
