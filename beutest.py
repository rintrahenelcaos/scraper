from bs4 import BeautifulSoup
import requests
import certifi
import pprint

import sys

import ast

url = "https://iol.invertironline.com/mercado/cotizaciones/argentina/cedears/todos" # tbody
url2 = "https://www.rava.com/cotizaciones/cedears"  #cedears-p
url3 = "https://www.bancopiano.com.ar/Inversiones/Cotizaciones/Cedears/" # tbody
url4 = "https://www.cohen.com.ar/Bursatil/Especie/AAL" #tbody
information = []

#response = requests.get(url, verify=certifi.where())
#print(response.text)

req = requests.get(url3)
#print(req.text)
soup = BeautifulSoup(req.text, 'html.parser')
#print(soup)
cedears_list = soup.tbody.find_all("tr")
#print(cedears[1].find_all("td")[0].attrs)
#print(cedears[1].find_all("td")[0]["title"])
#print(cedears[1].find_all("td")[0].text)
print(cedears_list[1].find_all("td")[-1].attrs)
print(cedears_list[2].find_all("td"))
for data in cedears_list[2].find_all("td"):
    print(data.text)
#print(cedears[1].find_all("td")[-1]["title"])
for cedear in cedears_list: pass
    #print(cedear)
    #for cedind in cedear.find_all("td"):
    #    print(cedind)
        #if "title" in cedind.attrs.keys():
        #    print(cedind.text)
#print(ced)
#print(cedears[1]["title"])
