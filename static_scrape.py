from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests

"""
data = requests.get("http://gameinfo.na.leagueoflegends.com/en/game-info/champions/ahri").text
soup = BeautifulSoup(data)
container = soup.find("div", "gs-container default-3-col")
skins = container.find_all("a", "skins")
del skins[0]

for skin in skins:
  print skin.get('title')
"""

data = requests.get("https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=all&api_key=01c86c6c-0907-434b-b8c9-d2762a953475")
print data.text
