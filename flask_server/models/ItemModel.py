from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
  __tablename__ = 'items'
  id = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String)
  name = db.Column(db.String)
  display_name = db.Column(db.String)
  splash_url = db.Column(db.String)

  def to_json(self):
    return {
      "id": self.id,
      "type": self.type,
      "name": self.name,
      "display_name": self.display_name
      "splash_url": self.splash_url
    }

  def from_json(self, source):
    if 'id' in source:
      self.id = source['id']
    if 'type' in source:
      self.type = source['type']
    if 'name' in source:
      self.name = source['name']
    if 'display_name' in source: 
      self.display_name = source['display_name']
    if 'splash_url' in source: 
      self.splash_url = source['splash_url']
