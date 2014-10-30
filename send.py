from pymongo import MongoClient
import sys
#asda
sale_url = sys.argv[1]
client = MongoClient('localhost', 27017)
db = client.skinsfarm
sales = db.sales
sale_data = sales.find_one({'href': sale_url})
  
print sale_data
