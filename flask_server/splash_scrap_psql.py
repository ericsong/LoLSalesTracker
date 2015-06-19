import psycopg2
import requests
from bs4 import BeautifulSoup

def addApos(string):
  return string.replace('\'', '\'\'')

con = psycopg2.connect(database='lolsalestracker', user='lolsalestracker_admin2', password='abc123')
cur = con.cursor()

cur.execute("SELECT * FROM items WHERE champ=key")

rows = cur.fetchall()

for row in rows:
  champ_key = row[1].lower()
  url = "http://gameinfo.na.leagueoflegends.com/en/game-info/champions/" + champ_key + "/"  
  data = requests.get(url)

  if data.status_code is not 200:
    print("Could not load: " + url)
    continue

  soup = BeautifulSoup(data.text)
  img_container = soup.find('div', 'gs-container default-3-col')
  skins_containers = img_container.find_all('a')
  
  for skin_c in skins_containers:
    img_url = skin_c.get('href')
    title = skin_c.get('title')

    if title == "":
      title = row[3]

    cur.execute("SELECT * FROM items WHERE name='" + addApos(title) + "'")
    matched_items = cur.fetchall()

    if len(matched_items) == 0:
      print("Could not find match for :" + title)

    matched_item = matched_items[0]
    cur.execute("UPDATE items SET splash_url='" + addApos(img_url) + "' WHERE name='" + addApos(title) + "'")

con.commit()

#verify valid img URLS
cur.execute("SELECT * FROM items")
items = cur.fetchall()
for item in items:
  img_url = item[4]
  if img_url is None:
    print(item)
  else:
    data = requests.get(img_url)
    if data.status_code is not 200:
      print("Invalid request: " + img_url)

con.close()
