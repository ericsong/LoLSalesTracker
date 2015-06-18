from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Sale(db.Model):
  __tablename__ = 'sales'
  id = db.Column(db.Integer, primary_key=True)
  create_time = db.Column(db.DateTime)
  start_time = db.Column(db.DateTime)
  end_time = db.Column(db.DateTime)
  href = db.Column(db.String)
  title = db.Column(db.String)
  items = db.relationship('SaleItem', backref='sale', lazy='dynamic')

class SaleItem(db.Model):
  __tablename__ = 'saleitems'
  id = db.Column(db.Integer, primary_key=True)
  sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'))
  item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
  price = db.Column(db.Integer)
