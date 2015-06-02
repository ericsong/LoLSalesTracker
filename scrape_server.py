from pymongo import MongoClient
import threading
import scrape as LWL

client = MongoClient('localhost', 27017)
db = client.lolwishlist
db_sales = db.sales

def f():
  # do something here ...
  sales = LWL.checkForNewSales()
  for sale in sales:
    #upload to database
    print sale['title']
    print sale['champs']
    print sale['skins']
    db_sales.insert(sale);

  # call f() again in 60 seconds
  threading.Timer(60, f).start()

# start calling f now and every 60 sec thereafter
f()
