#https://stackoverflow.com/questions/9968091/save-html-source-code-to-file
import urllib.request
from bs4 import BeautifulSoup
import requests

def extractHTML(url):
    f = open('temphtml.txt', 'w')
    page = urllib.request.urlopen(url)
    pagetext = str(page.read())
    f.write(pagetext)
    f.close()

extractHTML('https://es.investing.com/currencies/usd-pen')