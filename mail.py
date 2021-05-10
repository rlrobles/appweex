from flask import Flask
from flask_mail import Mail, Message

#https://stackoverflow.com/questions/24999277/trying-to-send-email-through-godaddy-using-python
#https://myaccount.google.com/lesssecureapps?pli=1
#https://myaccount.google.com/security?pmr=1
#https://stackoverflow.com/questions/23137012/535-5-7-8-username-and-password-not-accepted



app =Flask(__name__)
mail=Mail(app)

#app.config['MAIL_SERVER']='smtp.gmail.com'
#app.config['MAIL_PORT'] = 465

app.config['MAIL_SERVER']= 'localhost' #'smtpout.secureserver.net'
app.config['MAIL_PORT'] = 25 #465

#app.config['MAIL_USERNAME'] = 'royerleandroroblesvega@gmail.com'
#app.config['MAIL_PASSWORD'] = 'Synopsis2021.'

app.config['MAIL_USERNAME'] = 'rlrobles@demo.weex.pe'
app.config['MAIL_PASSWORD'] = 'DrXtASO?)BDx'

app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def index():
   msg = Message('Hello', sender = 'alonsoguzmanmurrugarra@gmail.com', recipients = ['royerleandroroblesvega@gmail.com'])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"

if __name__ == '__main__':
   app.run(debug = True)