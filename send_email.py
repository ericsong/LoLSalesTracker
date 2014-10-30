import os
import sendgrid

username = os.environ['sg_username']
password = os.environ['sg_password']

sg = sendgrid.SendGridClient(username, password)

message = sendgrid.Mail()
message.add_bcc(['eric.song@rutgers.edu'])
message.set_subject('An item on your wishlist is on sale!')
message.set_text('Yay!')
message.set_from('LoLWishList <info@lolwishlist.com>')
status, msg = sg.send(message)
print status
print msg
