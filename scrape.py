from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests

#grab page
data = requests.get("http://na.leagueoflegends.com/en/news/store/sales").text
soup = BeautifulSoup(data)
items = soup.find_all("div", "gs-container")
scraped_sales = []

#scrape sale data
for item in items:
  temp = item.find("div", "default-2-3")
  if(temp is not None):
    a_link = temp.find("a")
    scraped_sales.append((a_link.string, a_link.get('href')))

#get currently grabbed sales
client = MongoClient('localhost', 27017)
db = client.grandpateemo
sales = db.sales
db_sales = []

for sale in sales.find():
  db_sales.append((sale['title'], sale['href']))

#find new sales
new_sale = set(scraped_sales).difference(set(db_sales))

#do a thing
for sale in new_sale:
  print sale
