import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#sender_email_address = 'alonsoguzmanmurrugarra@gmail.com'
#sender_email_password = 'alonso27*'

sender_email_address = 'rlrobles@demo.weex.pe'
sender_email_password = 'DrXtASO?)BDx'

#receiver_email_address = 'royer.robles@outlook.com'
receiver_email_address = ['royer.robles@outlook.com','mattewppe@hotmail.com','danielberrospicarmona@gmail.com']

#lstCopy = ['royer.robles@outlook.com','royerleandroroblesvega@gmail.com']

email_subject_line = 'subject'

msg = MIMEMultipart()
msg['From'] = sender_email_address
#msg['To'] = receiver_email_address
msg['To'] = 'royer.robles@outlook.com,mattewppe@hotmail.com,danielberrospicarmona@gmail.com,royerleandroroblesvega@gmail.com'
msg['Subject'] = email_subject_line

msg['Cc'] = 'royer.robles@outlook.com,mattewppe@hotmail.com,danielberrospicarmona@gmail.com'
#msg['Cc'] = ['royer.robles@outlook.com','mattewppe@hotmail.com','danielberrospicarmona@gmail.com']

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
#server = smtplib.SMTP('smtp-mail.outlook.com:587')
#server = smtplib.SMTP('smtpout.secureserver.net:465')
server = smtplib.SMTP('localhost:25')
server.starttls()
server.login(sender_email_address, sender_email_password)
server.sendmail(sender_email_address, receiver_email_address, email_body_content)
server.quit()