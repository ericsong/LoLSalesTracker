from bs4 import BeautifulSoup
from pymongo import MongoClient
import json
import requests

def insertItem(name, type):
  item = items.find_one({'name': name}) 
  if item is None:
    items.insert({
      'name': name,
      'type': type
    })

client = MongoClient('localhost', 27017)
db = client.grandpateemo
items = db.items

data = requests.get("https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=all&api_key=01c86c6c-0907-434b-b8c9-d2762a953475")
champions =  json.loads(data.text)['data']

for champ in champions:
  champ_data = champions[champ]
  skins = champ_data['skins']
  for skin in skins:
    if skin['name'] == 'default':
      insertItem(champ, 'champ')
    else: 
      insertItem(skin['name'], 'skin')
