
import requests

def sensor():
    """ Function for test purposes. """
    r = requests.get('http://demo.weex.pe/home')
    r.status_code
    print(r.status_code)
    print("Scheduler is alive!")

sensor()