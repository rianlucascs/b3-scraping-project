import requests
from bs4 import BeautifulSoup

response = requests.get('https://github.com/rianlucascs/b3-scraping-project/blob/master/data_processed/indices.py')

soup = BeautifulSoup(response.text, 'html.parser')

content = soup.find(id='read-only-cursor-text-area')

print(content.get_text())

