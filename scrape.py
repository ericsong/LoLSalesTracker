from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests

def isNormalSale(sale):
  title = sale[0]
  if("Champion and skin sale" in title):
    return True
  else:
    return False

def isPrice(line):
  if("RP" in line):
    return True
  else:
    return False

def cleanString(str):
  return unicode(str).strip()

def scrapeSales(soup):
  container = soup.find("div", "field field-name-body field-type-text-with-summary field-label-hidden")
  headers = container.find_all("h4")

  skinNames = [headers[1].string, headers[2].string, headers[3].string]
  champNames = [headers[5].string, headers[6].string, headers[7].string]

  skinPrices = filter(isPrice, headers[1].parent.contents)
  champPrices = [ filter(isPrice, headers[5].parent.contents)[0],
                  filter(isPrice, headers[6].parent.contents)[0],
                  filter(isPrice, headers[7].parent.contents)[0] ]

  skins = []
  champs = []

  for i in range(0,3):
    skins.append((cleanString(skinNames[i]), cleanString(skinPrices[i])))
    champs.append((cleanString(champNames[i]), cleanString(champPrices[i])))

  sale = {
    "skins": skins,
    "champs": champs
  }

  return sale

#grab page
data = requests.get("http://na.leagueoflegends.com/en/news/store/sales").text
soup = BeautifulSoup(data)
items = soup.find_all("div", "gs-container")
scraped_sales = []

#scrape sale data  ("title", "href")
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
new_sales = set(scraped_sales).difference(set(db_sales))

#filter out non regular sales (for now)
new_sales = filter(isNormalSale, new_sales) 

#do a thing
for sale in new_sales:
  data = requests.get("http://na.leagueoflegends.com" + sale[1]).text
  soup = BeautifulSoup(data) 
  scraped_data = scrapeSales(soup)
  sales.insert({
    "href": sale[1],
    "title": sale[0],
    "skins": scraped_data["skins"],
    "champs": scraped_data["champs"]
  })

  #schedule sending script
