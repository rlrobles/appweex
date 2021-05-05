import requests
import json
#response = requests.get("http://localhost:5000/weex/tasa-cambio/v1")

payload = {
    "id": 1,
    "compra": 3.428,
    "venta": 3.442
}
body = json.dumps(payload)
print("body:", body)
response = requests.post('http://localhost:5000/weex/actualizar/tasa-cambio/v1', data = body)


print(response.json())