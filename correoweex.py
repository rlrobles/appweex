import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


sender_email_address = 'rlrobles@demo.weex.pe'
sender_email_password = 'DrXtASO?)BDx'

"""
receiver_email_address = 'royer.robles@outlook.com' #Support Array
email_subject_line = 'Recuperacion de contraseña - Weex'
msg = MIMEMultipart()
msg['From'] = sender_email_address
msg['To'] = receiver_email_address
msg['Subject'] = email_subject_line
msg['Cc'] = ''
email_body = html_content
msg.attach(MIMEText(email_body, 'plain'))
"""

"""
filename = 'sample_file.txt'
attachment_file = open('sample_file.txt', 'rb')
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment_file).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment_file; filename = "+filename)
msg.attach(part)
"""

"""
email_body_content = msg.as_string()
server = smtplib.SMTP('localhost:25')
server.starttls()
server.ehlo()
server.login(sender_email_address, sender_email_password)
server.sendmail(sender_email_address, receiver_email_address, email_body_content)
server.quit()
print("EXITO")
"""

def enviarCorreo(params, correo, contenido):
    print(params)
    print("ingreso fun")
    #receiver_email_address = 'royerleandroroblesvega@gmail.com' #Support Array
    receiver_email_address = correo #Support Array
    email_subject_line = 'Recuperacion de contraseña - Weex'

    msg = MIMEMultipart()
    msg['From'] = sender_email_address
    msg['To'] = receiver_email_address #params['receiver_email_address']
    msg['Subject'] = email_subject_line
    msg['Cc'] = ''

    print("---------------------")
    print(params['receiver_email_address'])
    print(params['html_content'])

    email_body = contenido #params['html_content']
    msg.attach(MIMEText(email_body, 'plain'))

    """
    filename = 'sample_file.txt'
    attachment_file = open('sample_file.txt', 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment_file).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment_file; filename = "+filename)
    msg.attach(part)
    """

    email_body_content = msg.as_string()
    print("antes de probar conexion")
    server = smtplib.SMTP('localhost:25')
    server.starttls()
    server.ehlo()
    server.login(sender_email_address, sender_email_password)
    server.sendmail(sender_email_address, receiver_email_address, email_body_content)
    server.quit()

    response = {
        "status_code": "000",
        "body": params['html_content'],
        "headers": []
    }

    print("Correo Enviado")

    return response