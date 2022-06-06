from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from flask import Flask

# Configure API key authorization: api-key
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'

# Uncomment below lines to configure API key authorization using: partner-key
# configuration = sib_api_v3_sdk.Configuration()
# configuration.api_key['partner-key'] = 'YOUR_API_KEY'

app = Flask(__name__) 


@app.route('/envioSendBlue')
def envioSendBlue():

   # create an instance of the API class
   api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
   subject = "Prueba Envio"
   send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[{"email":"allisonalvarez23@gmail.com","name":"Allison"}], 
   template_id=1, params={"nameClient":"Allison","docs":"docs"}, 
   headers={"X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3", 
   "charset": "iso-8859-1"}) # SendSmtpEmail | Values to send a transactional email   
   
   try:
      api_response = api_instance.send_transac_email(send_smtp_email)
      pprint(api_response)
   except ApiException as e:
      print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
    
   return 'Enviando'

def sendMailOperationConfirm(email, nombre, template):   
   # create an instance of the API class
   api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
   ##send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[{"email":"ayrtonjd0204@gmail.com","name":nombre}], 
   send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[{"email":email,"name":nombre}], 
   template_id= template, params={"nameClient":nombre,"docs":"docs"}, 
   headers={"X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3", 
   "charset": "iso-8859-1"}) # SendSmtpEmail | Values to send a transactional email   
   
   try:
      api_response = api_instance.send_transac_email(send_smtp_email)
      pprint(api_response)
   except ApiException as e:
      print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
    
   return 'Enviando'

def sendMailResetPassword(email, nombre, idClient, tokenClient, uribase):   
   # create an instance of the API class
   api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
   ##send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[{"email":"ayrtonjd0204@gmail.com","name":nombre}], 
   send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[{"email":email,"name":nombre}], 
   template_id= 3, params={"nameClient":nombre,"idClient":idClient,"tokenClient":tokenClient,"uribase":uribase,"path":"reset_password"}, 
   headers={"X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3", 
   "charset": "iso-8859-1"}) # SendSmtpEmail | Values to send a transactional email   
   
   try:
      api_response = api_instance.send_transac_email(send_smtp_email)
      pprint(api_response)
   except ApiException as e:
      print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
    
   return 'Enviando'

@app.route('/')
def hello_world():
   return 'Hello World'



if __name__ == '__main__':
   app.run()
   


