from bs4 import BeautifulSoup
import requests
import pprint

url = "https://www.cohen.com.ar/Bursatil/Especie/AAL"

result = requests.get(url)

soup = BeautifulSoup(result.text, 'html.parser')

cedears = soup.findAll("option")
a=0
for ind in cedears:
    print(ind.string)
    a+=1
    
    
#print(cedears)
print(len(cedears))