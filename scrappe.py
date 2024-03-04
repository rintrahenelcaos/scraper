from bs4 import BeautifulSoup
import requests

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(PPP)"

result = requests.get(url)

soup = BeautifulSoup(result.text, 'html.parser')

for table in soup.find_all('table'):
    print(table.get('class'))

tables = soup.find_all('table')

table = soup.find('table', class_='wikitable sortable sticky-header static-row-numbers')

print(table)

