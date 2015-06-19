import psycopg2
import os
import sys
import json
import requests

con = None

con = psycopg2.connect(database='lolsalestracker', user='lolsalestracker_admin2', password='abc123')
cur = con.cursor()

def addApos(string):
  return string.replace('\'', '\'\'')

def insertItem(champ, name, key, id):
  try:
    cur.execute("INSERT INTO items VALUES(" + str(id) + ", '" + addApos(key) + "', '" + addApos(champ) + "', '" + addApos(name) + "')")
  except psycopg2.DatabaseError as e:
    if con:
      con.rollback()
    print('something fucked up')
    print(e)
    sys.exit(1)

def init_db():
  with app.app_context():
    db.create_all()

LOL_API_KEY = os.environ['LOL_API_KEY']

data = requests.get("https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=all&api_key=" + LOL_API_KEY)
champions =  json.loads(data.text)['data']

for champ in champions:
  champ_data = champions[champ]
  skins = champ_data['skins']

  insertItem(champ, champ_data['name'], champ_data['key'], champ_data['id'])
  for skin in skins:
    if(skin['name'] == "default"):
      insertItem(champ, champ, champ, skin['id'])
    else:
      insertItem(champ, skin['name'], skin['name'], skin['id'])

con.commit()
con.close()
