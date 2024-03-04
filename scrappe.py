from bs4 import BeautifulSoup
import requests

url = "https://www.cohen.com.ar/Bursatil/Especie/AAL"

result = requests.get(url)

soup = BeautifulSoup(result.text, 'html.parser')

"""tabla = soup.find_all('div', id= "CotizacionesUltimaOperacion")
print(tabla)"""

"""for div in soup.find_all('div'):
    print(div.get('class'))"""

"""tables = soup.find_all('table')

table = soup.find('table', class_='wikitable sortable sticky-header static-row-numbers')

print(table)
"""
information = []
"""symb=soup.h2
symbol = symb.contents"""
symbol = soup.find("h2").contents
print(symbol)
information.append(soup.find("h2").contents[0])
print(information)

description = soup.find(class_="tdDescripcionNombre").contents
print(description)

def scrapper(url_list, codes_list):
    
    for ind_url in url_list:
        req =requests.get(ind_url)
        soup = BeautifulSoup(result.text, 'html.parser')
        for code in codes_list:
            information.append(soup.find(code).contens[0])
        scrapped.append(information)
        
        


