from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WishlistItem(db.Model):
  __tablename__ = 'wishlistItem'
  user = db.Column(db.String) #FK to 'users'
  item = db.Column(db.Integer) #FK to 'items'
  #active (boolean)
  #time_created (datetime)
  #time_deactivated
