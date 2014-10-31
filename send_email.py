import os
import sendgrid

username = os.environ['sg_username']
password = os.environ['sg_password']

sg = sendgrid.SendGridClient(username, password)

message = sendgrid.Mail()
message.add_to('eric.song@rutgers.edu')
message.set_subject('hi')
message.set_html('Body')
message.set_text('Body')
message.set_from('Eric Song <blah blah blah@eric-song.com>')
message.smtpapi.set_schedule(1414648800)
status, msg = sg.send(message)
