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
    #print(contentPage)
    #print(statusCode)
    soup = BeautifulSoup(contentPage, "html.parser")
    #print(soup.find(id='last_last'))
    ##changeRate = soup.find(id='last_last')
    changeRateBuy = soup.find('span', class_='inlineblock pid-2177-bid')
    changeRateBuy = changeRateBuy.string

    changeRateSale = soup.find('span', class_= 'inlineblock pid-2177-ask')
    changeRateSale = changeRateSale.string

    return changeRateBuy, changeRateSale