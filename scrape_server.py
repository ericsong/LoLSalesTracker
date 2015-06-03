from pymongo import MongoClient
import threading
import scrape as LWL
import os
import sys
import sendgrid

#db setup
client = MongoClient('localhost', 27017)
db = client.lolwishlist
db_sales = db.sales
db_items = db.items
db_users = db.users

#sendgrid setup
sg_username = os.environ['sg_username']
sg_password = os.environ['sg_password']
sg = sendgrid.SendGridClient(sg_username, sg_password)

#def generateEmailBody(items, sale):
    #template = """<div dir=3D"ltr">An item from your wishlist, <b>Nightblade Irelia</b>, will be on sale for 400 RP from 6/02 ~ 6/05.<br><br>You will no longer receive email alerts when <b>Nightblade Irelia </b>goes on sale<b>. </b>If you wish to keep tracking this item, please <a href=3D"https://www.google.com">click here.</a><br><br><div><b>Champion and Skin Sales: 5/29 ~ 6/3</b></div><div>Zac - 440 RP</div><div>Swain - 440 RP</div><div>Miss Fortune - 395 RP</div><div>Shockblade Zed - 487 RP</div><div>Arcade Hecarim - 487 RP</div><div>Commando Jarvan IV - 487 RP<br><br><a href=3D"http://na.leagueoflegends.com/en/news/store/sales/champion-and-skin-sale-0526-0529">Official Link</a><br><br><a href=3D"http://www.google.com">Click here</a> to unsubscribe form this service.</div></div>"""

def checkForNewSales():
  #grab new sales
  sales = LWL.getNewSales()
  for sale in sales:
    #upload to database
    print sale['title']
    print sale['champs']
    print sale['skins']
    db_sales.insert(sale);

    #generate item basket with item ids
    saleIds = []
    for champ in sale['champs']:
      matched_item = db_items.find_one({"display_name": champ[0]})
      if matched_item:
        saleIds.append(matched_item['id'])
      else:
        print "no match error"

    for champ in sale['skins']:
      matched_item = db_items.find_one({"display_name": champ[0]})
      if matched_item:
        saleIds.append(matched_item['id'])
      else:
        print "no match error"

    print saleIds
    #find users that need to be emailed 
    
    matched_users = db_users.find({"wishlist": { "$in": saleIds }})
    for user in matched_users:
      print user
  # call f() again in 60 seconds
  threading.Timer(60, checkForNewSales).start()

# start calling f now and every 60 sec thereafter
checkForNewSales()
