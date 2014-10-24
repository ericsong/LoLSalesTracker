from pymongo import MongoClient
import sys

sale_url = sys.argv[1]
client = MongoClient('localhost', 27017)
db = client.grandpateemo
sales = db.sales
sale_data = sales.find_one({'href': sale_url})
for skin in sale_data['skins']:
  
print sale_data
