from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import os

def getContentPage(url):
    req = Request(url, headers={'User-Agent': 'XYZ/3.0'})
    webpage = urlopen(req, timeout=10).read()
    soup = BeautifulSoup(webpage, "html.parser")
    changeRate = soup.find(id='last_last')
    changeRateText = changeRate.string
    print(changeRateText)

getContentPage('https://es.investing.com/currencies/usd-pen')