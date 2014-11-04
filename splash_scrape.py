from pymongo import MongoClient
import requests

client = MongoClient('localhost', 27017)
db = client.skinsfarm
items = db.items

champs = items.find({'type': 'champ'})

for champ in champs:
  champ_key = champ['key'].lower()
  url = "http://gameinfo.na.leagueoflegends.com/en/game-info/champions/" + champ_key + "/"  
  data = requests.get(url)
