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
    changeRateB = soup.find_all('div', class_='inlineblock pid-2177-bid')
    
    changeRateBuy = changeRateB.string

    changeRateS = soup.find_all('div', class_= 'inlineblock pid-2177-ask')
    changeRateSale = changeRateS.string

    #print(changeRateText)
    return changeRateBuy, changeRateSale