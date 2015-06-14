from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  order = db.Column(db.Integer)
  completed = db.Column(db.Boolean)

  def to_json(self):
    return {
      "id": self.id,
      "title": self.title,
      "order": self.order,
      "completed": self.completed
    }

  def from_json(self, source):
    if 'title' in source:
      self.title = source['title']
    if 'order' in source:
      self.order = source['order']
    if 'completed' in source: 
      self.completed = source['completed']
