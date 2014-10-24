from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.grandpateemo
sales = db.sales

sale =  {
          "href": "/en/news/store/sales/champion-and-skin-sale-1021-1024",
          "title": "Champion and skin sale: 10.21. - 10.24."
        }

sales.insert(sale)
