from bs4 import BeautifulSoup
import requests
import os

url = "https://es.investing.com/currencies/usd-pen"
response = requests.get(url)
responseText = response.text

print(responseText)


soup = BeautifulSoup(responseText, "html.parser")
print(soup.title)

#cmd = 'date'
#command = responseText + '>' + 'resulFile.txt'
#os.system(command)

#soup = BeautifulSoup(req.text, "html.parser")
#print(soup.title)