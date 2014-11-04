from bs4 import BeautifulSoup
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
  soup = BeautifulSoup(data.text)
  img_container = soup.find('div', 'gs-container default-3-col')
  skins_containers = img_container.find_all('a')
  
  for skin_c in skins_containers:
    img_url = skin_c.get('href')
    title = skin_c.get('title')

    if title == "":
      title = champ['name']
    else:
      title = "".join(skin_c.get('title').split()).lower()
 
    matched_item = items.find_one({'name': title})

    if matched_item is not None:
      matched_item['splash_url'] = img_url

    items.save(matched_item)
