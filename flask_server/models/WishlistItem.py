from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WishlistItem(db.Model):
  __tablename__ = 'wishlistItem'
  user = db.Column(db.String, db.ForeignKey('user.id'))
  item = db.Column(db.Integer, db.ForeignKey('item.id'))
  create_time = db.Column(db.DateTime)
  deactivated_time = db.Column(db.DateTime)
  active = db.Column(db.Boolean, default=True)
