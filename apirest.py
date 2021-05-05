import schedule
import time
import requests
import json

def job():
    print("I'm working...")
    #url = 'http://localhost:5000/weex/actualizar/tasa-cambio/v1'
    url = 'http://localhost:5000/weex/actualizar/tasa-cambio/v1'
    myobj = {
        "id": 1,
        "compra": 3.428,
        "venta": 3.44
    }
    payload = json.dumps(myobj)
    print(type(payload))
    #res = requests.post(url, data = {'id':1,'compra':3.428,'venta':3.44})
    res = requests.get(url)
    print(res.text)

job()