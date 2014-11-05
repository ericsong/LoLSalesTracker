from pymongo import MongoClient
import os
import json
import requests

LOL_API_KEY = os.environ['LOL_API_KEY']

def insertChamp(name, key, id):
  item = items.find_one({'id': id}) 
  if item is None:
    items.insert({
      'name': "".join(name.split()).lower(),
      'champ': "".join(name.split()).lower(),
      'display_name': name,
      'key': key,
      'id': id,
      'type': 'champ'
    })

def insertSkin(name, champ, id):
  item = items.find_one({'id': id}) 
  if item is None:
    items.insert({
      'name': "".join(name.split()).lower(),
      'champ': "".join(champ.split()).lower(),
      'display_name': name,
      'id': id,
      'type': 'skin'
    })

client = MongoClient('localhost', 27017)
db = client.skinsfarm
items = db.items

data = requests.get("https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=all&api_key=" + LOL_API_KEY)
champions =  json.loads(data.text)['data']

for champ in champions:
  champ_data = champions[champ]
  skins = champ_data['skins']
  for skin in skins:
    if skin['name'] == 'default':
      insertChamp(champ_data['name'], champ, skin['id'])
    else: 
      insertSkin(skin['name'], champ_data['name'], skin['id'])
