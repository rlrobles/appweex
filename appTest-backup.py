from flask import Flask
from flask_mail import Mail, Message  # Importamos la clase Mail

import weexConstants
from mailin import Mailin 

app = Flask(__name__) 

mail = Mail()  # Instanciamos un objeto de tipo Mail

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

app.config.update(
    MAIL_SERVER = weexConstants.MAIL_SERVER,
    MAIL_PORT = weexConstants.MAIL_PORT,
    MAIL_USE_TLS = weexConstants.MAIL_USE_TLS,
    MAIL_USERNAME = weexConstants.MAIL_USERNAME,
    MAIL_PASSWORD = weexConstants.MAIL_PASSWORD
)
mail = Mail(app) 



@app.route('/envioCorreo')
def envioCorreo():
   msg = Message( 
                'Hello', 
                sender ='notificacion@weex.pe', 
                recipients = ['ayrtonjd0204@gmail.com'] 
               ) 
   msg.body = 'Hello Flask message sent from Flask-Mail'
   mail.send(msg) 
   return 'Enviando'

@app.route('/envioSendBlue')
def envioSendBlue():
   m = Mailin("https://api.sendinblue.com/v3.0","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")
   data = { "to" : {"ayrtonjd0204@gmail.com":"Jordan Ocmin"},
		"from" : ["notificacion@weex.pe", "Notificacion Weex"],
		"subject" : "Primer Envio",
		"html" : "This is the <h1>HTML</h1>"
	}

   result = m.send_email(data)
   print(result)

   return 'Enviando'


@app.route('/')
def hello_world():
   return 'Hello World'



if __name__ == '__main__':
   app.run()
   mail.init_app(app)  # Inicializamos el objeto mail



