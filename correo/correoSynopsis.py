import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

sender_email_address = 'rlrobles@synopsis.ws'
sender_email_password = 'nuevo2018'
receiver_email_address = 'royer.robles@outlook.com'


#lstCopy = ['royer.robles@outlook.com','royerleandroroblesvega@gmail.com']

email_subject_line = 'subject'

msg = MIMEMultipart()
msg['From'] = sender_email_address
msg['To'] = receiver_email_address
msg['Subject'] = email_subject_line

#msg['Cc'] = 'royer.robles@outlook.com'

email_body = 'Hello World. This is Python email sender application with Attachments.'
msg.attach(MIMEText(email_body, 'plain'))

filename = 'sample_file.txt'
attachment_file = open('sample_file.txt', 'rb')
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment_file).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment_file; filename = "+filename)

msg.attach(part)

email_body_content = msg.as_string()
server = smtplib.SMTP('smtp.scotty.synopsis.ws:587')
server.starttls()
server.login(sender_email_address, sender_email_password)
server.sendmail(sender_email_address, receiver_email_address, email_body_content)
server.quit()