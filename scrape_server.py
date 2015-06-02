from pymongo import MongoClient
import threading
import scrape as LWL
import os
import sendgrid

#db setup
client = MongoClient('localhost', 27017)
db = client.lolwishlist
db_sales = db.sales

#sendgrid setup
sg_username = os.environ['sg_username']
sg_password = os.environ['sg_password']
sg = sendgrid.SendGridClient(sg_username, sg_password)

def f():
  # do something here ...
  sales = LWL.checkForNewSales()
  for sale in sales:
    #upload to database
    print sale['title']
    print sale['champs']
    print sale['skins']
    db_sales.insert(sale);
   
    #generate email body
    email_body = ""
    email_body += "Sale from " + sale['title'] + "\n\n\n"

    email_body += "Champions: " + "\n"
    for champ in sale['champs']:
      email_body += champ[0] + ": " + champ[1] + "\n"

    email_body += "Skins: " + "\n"
    for skin in sale['skins']:
      email_body += skin[0] + ": " + skin[1] + "\n"

    #generate email
    message = sendgrid.Mail()
    message.add_to('regonics@gmail.com')
    message.set_subject('New League of Legends Skin/Champion sale!')
    message.set_text(email_body)
    message.set_from("LoLSalesTracker <tracker@lolsalestracker.com>")
    status, msg = sg.send(message)

    print status

  # call f() again in 60 seconds
  threading.Timer(60, f).start()

# start calling f now and every 60 sec thereafter
f()
