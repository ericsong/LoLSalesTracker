from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.lolwishlist
users = db.users
db_items = db.items

#get all champions
champs = db_items.find({'type': "champ"})

counter = 0
user_count = 1;
wishlist = []
for champ in champs:
    items = db_items.find({'champ': champ['champ']})
    for item in items:
        wishlist.append(item['id'])

    counter = counter + 1

    if counter == 5:
        users.insert({
            'email': 'regonics+lolsalestracker_' + str(user_count) + '@gmail.com',
            'wishlist': wishlist,
            'verified': True
        })

        user_count = user_count + 1
        counter = 0
        wishlist = []
