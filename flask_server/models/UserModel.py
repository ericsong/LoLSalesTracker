from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  email = db.Column(db.String, primary_key=True)
  uuid = db.Column(db.String, unique=True)
  verified = db.Column(db.Boolean)

  def to_json(self):
    return {
      "email": self.email,
      "uuid": self.uuid,
      "verified": self.verified,
      #created_datetime
      #send_emails, boolean
    }

  def from_json(self, source):
    if 'email' in source:
      self.email = source['email']
    if 'uuid' in source:
      self.uuid = source['uuid']
    if 'verified' in source:
      self.verified = source['verified']
