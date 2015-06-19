from .extensions import db

class Item(db.Model):
  __tablename__ = 'items'
  id = db.Column(db.Integer, primary_key=True)
  key = db.Column(db.String)
  champ = db.Column(db.String)
  name = db.Column(db.String)
  splash_url = db.Column(db.String)

  def to_json(self):
    return {
      "id": self.id,
      "type": self.type,
      "name": self.name,
      "display_name": self.display_name,
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
  sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'))
  item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
  price = db.Column(db.Integer)

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  create_time = db.Column(db.DateTime)
  email = db.Column(db.String, unique=True)
  uuid = db.Column(db.String, unique=True)
  verified = db.Column(db.Boolean, default=False)
  wants_emails = db.Column(db.Boolean, default=True)
  wishlist_items = db.relationship('WishlistItem', backref='users', lazy='dynamic')

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

class WishlistItem(db.Model):
  __tablename__ = 'wishlistitems'
  id = db.Column(db.Integer, primary_key=True)
  user = db.Column(db.Integer, db.ForeignKey('users.id'))
  item = db.Column(db.Integer, db.ForeignKey('items.id'))
  create_time = db.Column(db.DateTime)
  deactivated_time = db.Column(db.DateTime)
  active = db.Column(db.Boolean, default=True)
