
import requests
import webscraping
from datetime import datetime
from datetime import timedelta
import json

def sensor():
    """ Function for test purposes. """
    r = requests.get('http://demo.weex.pe/home')
    r.status_code
    print(r.status_code)
    print("Scheduler is alive!")

def apiUpdateTipoCambioInvesting(payload):
    #url = 'http://localhost:5000/weex/actualizar/tasa-cambio/v1'
    url = 'http://demo.weex.pe/weex/actualizar/tasa-cambio/v1'
    body = json.dumps(payload)
    #print("body:", body)
    header = {'content-type': 'application/json'}
    response = requests.post(url, headers = header,  data = body)
    print(response.status_code)
    print("Ejecución Exitosa de Actualización de Tipo de Cambio")
    return response.json()

def getTipoCambioInvesting(url):
    tipoCambioCompra,tipoCambioVenta  = webscraping.getContentPage(url)
    tipoCambioCompra = tipoCambioCompra.replace(",", ".")
    tipoCambioVenta = tipoCambioVenta.replace(",", ".")

    print(tipoCambio)
    return tipoCambioCompra, tipoCambioVenta

def jobUpdateTipoCambio():
    print("I'm working...")
    now = datetime.now()
    print(now)
    valorTipoCambioCompra, valorTipoCambioVenta = getTipoCambioInvesting('https://es.investing.com/currencies/usd-pen')
    data = {
        "id": 1,
        "compra": valorTipoCambio,
        "venta": valorTipoCambioVenta
    }
    print(data)
    response = apiUpdateTipoCambioInvesting(data)
    print(response)

jobUpdateTipoCambio()