from pymongo import MongoClient
import psycopg2
import threading
import scrape as LWL
import os
import sys
import sendgrid

def addApos(string):
  return string.replace('\'', '\'\'')

#db setup
client = MongoClient('localhost', 27017)
db = client.lolwishlist
db_sales = db.sales
db_items = db.items
db_users = db.users

con = psycopg2.connect(database='lolsalestracker', user='lolsalestracker_admin2', password='abc123')
cur = con.cursor()

#sendgrid setup
sg_username = os.environ['sg_username']
sg_password = os.environ['sg_password']
sg = sendgrid.SendGridClient(sg_username, sg_password)

def extractDatesFromTitle(title):
  return title.split(':')[1][1:]

def generateEmailContent(user, sale):
  #find items in wishlist that are on sale
  saleIds = set(sale['itemIds']).intersection(user['wishlist'])
  saleItems = []
  dateString = extractDatesFromTitle(sale['title'])

  #transform ids into saleItem objects with display name, Rp price
  for item in saleIds:
    qs = cur.execute("SELECT * FROM items where id=" + str(item))
    matched_db_item = (cur.fetchall())[0]

    for skin in sale['skins']:
      if matched_db_item[3] == skin[0]:
        matched_item = skin
    for champ in sale['champs']:
      if matched_db_item[3] == champ[0]:
        matched_item = champ

    item = {
      'name': matched_db_item[3],
      'id': item,
      'cost': matched_item[1]
    }

    saleItems.append(item)

  print(saleItems)
  sys.exit(1)

  #generate email subject
  if len(saleItems) == 1:
    subject = saleItems[0]['name'] + " is on sale!"
  elif len(saleItems) == 2:
    subject = saleItems[0]['name'] + " and " + saleItems[1]['name'] + " are on sale!"
  else:
    subject = saleItems[0]['name']

    for item in saleItems[1:]:
      subject += ", " + item['name']

    subject += " are on sale!"

  subject += " (" + dateString + ")"

  #generating email body
  isMultiple = True if len(saleItems) > 1 else False

  if isMultiple:
    listHTML =  """<div dir="ltr">Items from your wishlist will be on sale from """ +\
                dateString +\
                """:<br>"""
  else:
    listHTML =  """<div dir="ltr">An item from your wishlist will be on sale from """ +\
                dateString +\
                """:<br>"""

  for item in saleItems:
    listHTML += "-<b>" + item['name'] + " : " + item['cost'] + "</b><br>"

  if isMultiple:
    #keepTrackingHTML = """ <br>You will no longer receive email alerts when these items go on sale. If you wish to keep tracking them, please """
    keepTrackingHTML = """ <br>You will no longer receive email alerts when these items go on sale. """
  else:
    #keepTrackingHTML = """ <br>You will no longer receive email alerts when this item goes on sale. If you wish to keep tracking it, please """
    keepTrackingHTML = """ <br>You will no longer receive email alerts when this item goes on sale. """

  #keepTrackingHTML +=  """<a href="https://www.google.com">click here.</a>"""

  saleListHTML = "<br><br><div><i>Champion and Skin Sales: " + dateString + "</i></div>"
  for champ in sale['champs']:
    saleListHTML += "<div>" + champ[0] + " - " + champ[1] + "</div>"
  for skin in sale['skins']:
    saleListHTML += "<div>" + skin[0] + " - " + skin[1] + "</div>"

  saleListHTML += """<br><a href="http://na.leagueoflegends.com""" + sale['href'] + """">Official Link</a><br><br>"""
  
  unsubscribeHTML = """<a href="http://www.google.com">Click here</a> to unsubscribe form this service.</div></div>"""

  return {
    'subject': subject,
    'body': listHTML + keepTrackingHTML + saleListHTML + unsubscribeHTML
  }

def checkForNewSales():
  #grab new sales
  sales = LWL.getNewSales()
  for sale in sales:
    #upload to database
    print(sale['title'])
    print(sale['champs'])
    print(sale['skins'])
    db_sales.insert(sale);

    #generate item basket with item ids
    saleIds = []
    saleNames = []
    for champ in sale['champs']:
      qs = cur.execute("SELECT * FROM items where name='" + addApos(champ[0]) + "'")
      matched_item = (cur.fetchall())[0]
      if matched_item:
        saleIds.append(matched_item[0])
        saleNames.append(champ[0])
      else:
        print("no match error")

    for skin in sale['skins']:
      qs = cur.execute("SELECT * FROM items where name='" + addApos(skin[0]) + "'")
      matched_item = (cur.fetchall())[0]
      if matched_item:
        saleIds.append(matched_item[0])
        saleNames.append(skin[0])
      else:
        print("no match error")

    sale['itemIds'] = saleIds
    sale['itemNames'] = saleNames

    #find users that need to be emailed 
    matched_users = db_users.find({"wishlist": { "$in": saleIds }})
    for user in matched_users:
      emailContent = generateEmailContent(user, sale)

      message = sendgrid.Mail()
      message.add_to(user['email'])
      message.set_subject(emailContent['subject'])
      message.set_html(emailContent['body'])
      message.set_from('LoLSalesTracker <tracker@lolsalestracker.com>')
      status, msg = sg.send(message);
      print(status)

  # call f() again in 60 seconds
  threading.Timer(60, checkForNewSales).start()

# start calling f now and every 60 sec thereafter
checkForNewSales()
