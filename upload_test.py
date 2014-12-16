from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.lolwishlist
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

email = 'eric.song@rutgers.edu'
wishlist = [39000,39001,39002,39003,39004]
verified = True 

users.insert({
	'email': email,
	'wishlist': wishlist,
	'verified': verified
})

email = 'erichyunjoonsong@gmail.com'
wishlist = [120000,120001,120002,120003,120004]
verified = True

users.insert({
	'email': email,
	'wishlist': wishlist,
	'verified': verified
})
