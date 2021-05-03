from urllib.request import Request, urlopen
from urllib.error import HTTPError
import urllib.request
from bs4 import BeautifulSoup
import requests
import os

def getContentPage(url):
    req = Request(url, headers={'User-Agent': 'XYZ/3.0'})
    webpage = urlopen(req, timeout=10)
    contentPage = webpage.read()
    statusCode = webpage.getcode()
    print(contentPage)
    print(statusCode)
    soup = BeautifulSoup(contentPage, "html.parser")
    #print(soup.find(id='last_last'))
    changeRate = soup.find(id='last_last')
    changeRateText = changeRate.string
    print(changeRateText)

def existsValue(content):
    if content != "":
        print('ingreso aqui')
        return True
    else:
        return False

""" def getContentPage1(url):
    req = Request(url, headers={'User-Agent': 'XYZ/3.0'})
    webpage = urlopen(req, timeout=10).read()
    print(webpage.status )
    soup = BeautifulSoup(webpage, "html.parser")
    changeRate = soup.find(id='last_last')
    changeRateText = changeRate.string
    print(changeRateText)



def validateStatusCode(url):
    print('fff')
    response = urllib.request.urlopen(url)
    response_status = response.status # 200, 301, etc
    print(response_status) """
      

existsValue('<span class="arial_26 inlineblock pid-2177-last" dir="ltr" id="last_last">3,7833</span>')
getContentPage('https://es.investing.com/currencies/usd-pen')