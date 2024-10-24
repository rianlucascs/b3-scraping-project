import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.b3.com.br/pt_br/solucoes/plataformas/puma-trading-system/para-participantes-e-traders/horario-de-negociacao/acoes/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar a tabela
table = soup.find('table', class_='responsive')

# Extrair cabeçalhos
headers = []
for header in table.find_all('th'):
    header_text = header.get_text(strip=True)
    if header_text:
        headers.append(header_text)

# Extrair dados das linhas
data = []
for row in table.find_all('tr')[1:]:  # Ignora o cabeçalho
    cols = row.find_all('td')
    if cols:
        data.append([col.get_text(strip=True) for col in cols])


headers_2 = [[item] * 2 for item in headers[1:]]
flattened_list = [item for sublist in headers_2 for item in sublist]
flattened_list = [item for item in flattened_list if item != 'After-Market2']
flattened_list = [headers[0]] + flattened_list

lista = []
for i, item in enumerate(flattened_list):
    if i >= len(flattened_list) - 6:
        lista.append(f'After-Market2 {item}')
    else:
        lista.append(item)

lista2 = []
for i, item in enumerate(flattened_list):
    if i != 0:
        lista2.append(f'{item} "{data[0][i].upper()}"')
    else:
        lista2.append(item)
        
df = pd.DataFrame(data[1:], columns=lista2)
df.to_excel(r'C:\Users\xxis4\Desktop\b3-scraping-project\teste.xlsx')
print(df)