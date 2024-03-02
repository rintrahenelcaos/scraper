from bs4 import BeautifulSoup
import requests

url = "https://www.cohen.com.ar/Bursatil/Especie/BA.C"

result = requests.get(url)

doc = BeautifulSoup(result.text, "html.parser")
    
contenedor = doc.has_attr("id")
print(contenedor)