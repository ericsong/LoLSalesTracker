from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.skinsfarm
users = db.users

#upload data
email = 'regonics@gmail.com'
wishlist = [35002, 62004, 24000, 5900]
verified = True

users.insert({
  'email': email,
  'wishlist': wishlist,
  'verified': verified
})
