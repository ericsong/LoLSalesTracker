from pymongo import MongoClient
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import os
import sys
import sendgrid

#grab sendgrid credentials
username = os.environ['sg_username']
password = os.environ['sg_password']

#set up db connection
client = MongoClient('localhost', 27017)
db = client.skinsfarm
sales = db.sales
items = db.items
users = db.users

#set up email
sg = sendgrid.SendGridClient(username, password)
message = sendgrid.Mail()
message.set_subject('An item on your wishlist is on sale!')
message.set_text('Yay!')
message.set_from('LoLWishList <info@lolwishlist.com>')

#grab sale data
sale_url = sys.argv[1]
sale_data = sales.find_one({'href': sale_url})
sale_items = []

for champ in sale_data['champs']:
  matched_item = items.find_one({'name': "".join(champ[0].split()).lower()})
  sale_items.append(matched_item)

for skin in sale_data['skins']:
  matched_item = items.find_one({'name': "".join(skin[0].split()).lower()})
  sale_items.append(matched_item)

sale_ids = []
for sale in sale_items:
  sale_ids.append(sale['id'])

sale_ids.append(35002)

#grab notify list
users = users.find({'verified': True, 'wishlist': { '$in': sale_ids }})

notify_emails = []
for user in users:
  notify_emails.append(user['email'])

message.add_bcc(notify_emails)

#determine send time
start_date = sale_data['start_date']
print start_date
send_date = start_date + timedelta(hours=1)
send_date_epoch = int((send_date - datetime(1970,1,1)).total_seconds())
message.smtpapi.set_schedule(send_date_epoch)

#send emails
status, msg = sg.send(message)
print status
print msg
