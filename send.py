from pymongo import MongoClient
import sys

client = MongoClient('localhost', 27017)
db = client.skinsfarm
sales = db.sales
items = db.items
users = db.users

sale_url = sys.argv[1]
sale_data = sales.find_one({'href': sale_url})
sale_items = []

for champ in sale_data['champs']:
  matched_item = items.find_one({'name': "".join(champ[0].split()).lower()})
  sale_items.append(matched_item)

for skin in sale_data['skins']:
  matched_item = items.find_one({'name': "".join(skin[0].split()).lower()})
  sale_items.append(matched_item)

sale_ids = []
for sale in sale_items:
  sale_ids.append(sale['id'])

users = users.find({'wishlist': { '$in': sale_ids }})

for user in users:
  print user
