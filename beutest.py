from bs4 import BeautifulSoup
import requests
import certifi
import pprint

import sys

url = "https://iol.invertironline.com/mercado/cotizaciones/argentina/cedears/todos" # tbody
url2 = "https://www.rava.com/cotizaciones/cedears"  #cedears-p
url3 = "https://open.bymadata.com.ar/#/dashboard"
url4 = "https://bolsar.info/Cedears.php" #tbody
information = []

#response = requests.get(url, verify=certifi.where())
#print(response.text)

req = requests.get(url)
#print(req.text)
soup = BeautifulSoup(req.text, 'html.parser')
#print(soup)
cedears = soup.tbody

#pprint.pprint(cedears)

texto = cedears.find("td")
texto2 = texto.i
#print((texto.find("i")))
print(texto2)
print(texto2.parent.parent["data-tituloid"])
attribute = texto2["title"]
print(attribute)

cedears_list = (cedears.find_all("b"))
cedears_cured_list = []
cedears_data_tituloid = []
excluded_cedears = []
for cedear in cedears_list:
    if cedear.string == None:
        excluded_cedears.append(cedears_list.index(cedear))
    else:
        
        #print(cedear)
        #print((cedear.text).strip())
        cedears_cured_list.append((cedear.text).strip())    # list of cedears
        cedears_data_tituloid.append(cedear.parent.parent.parent["data-tituloid"])
        pass
    
print(cedears_cured_list)
#print(cedears_data_tituloid)
#print(excluded_cedears)
#print(cedears.find_all("b"))

for cedear in cedears_list:
    if( cedear.text).strip() == "AAL":
        print(cedear.parent.parent.parent["data-tituloid"])


    

cedear_data_list = []

for tituloid in cedears_data_tituloid:
    raw_data = cedears.find(attrs={"data-tituloid": tituloid})
    #print(len(raw_data))
    info = []
    info.append((raw_data.find("b").text).strip())
    info.append(raw_data.i["title"])
    info.append((raw_data.find(attrs = {"data-field":"UltimoPrecio"}).text.strip()))
    info.append((raw_data.find(attrs = {"data-field":"Variacion"}).text.strip()))
    info.append((raw_data.find(attrs = {"data-field":"Apertura"}).text.strip()))
    info.append((raw_data.find(attrs = {"data-field":"UltimoCierre"}).text.strip()))
    info.append((raw_data.find(attrs = {"data-field":"Minimo"}).text.strip()))
    info.append((raw_data.find(attrs = {"data-field":"Maximo"}).text.strip()))
    info.append((raw_data.find_all("td")[-2].text).strip())
    cedear_data_list.append(info)

print(cedear_data_list)
    
    


    