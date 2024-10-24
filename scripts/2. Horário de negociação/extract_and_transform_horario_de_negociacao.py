

from os.path import join, dirname, abspath
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame


class ExtractAndTransform:

    def __init__(self, path_processed_data):
        self.path_processed_data = path_processed_data
    
    def request_page(self):
        url = 'https://www.b3.com.br/pt_br/solucoes/plataformas/puma-trading-system/para-participantes-e-traders/horario-de-negociacao/acoes/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='responsive')
        return table

    def get_cabecalho(self, table):
        headers = []
        for header in table.find_all('th'):
            header_text = header.get_text(strip=True)
            if header_text:
                headers.append(header_text)
        return headers
    
    def get_data(self, table):
        data = []
        for row in table.find_all('tr')[1:]:  # Ignora o cabeçalho
            cols = row.find_all('td')
            if cols:
                data.append([col.get_text(strip=True) for col in cols])
        return data
    
    def transform_cabecalho(self, cabecalho, data):
        # Duplicar os headers, exceto o primeiro
        headers = [[item] * 2 for item in cabecalho[1:]]

        # Achatar a lista e remover 'After-Market2'
        flattened_list = [item for sublist in headers for item in sublist if item != 'After-Market2']

        # Adicionar o primeiro header de volta
        flattened_list = [cabecalho[0]] + flattened_list

        # Criar a lista 'lista' com 'After-Market2' nos últimos 6 itens
        lista = [
             f'After-Market2 {item}' if i >= len(flattened_list) -6 else item 
             for i, item in enumerate(flattened_list)
        ]
        # Criar a lista 'lista2' formatando os itens
        lista2 = [
            item if i == 0 else f'{item} "{data[0][i].upper()}"'
            for i, item in enumerate(lista)
        ]

        return lista2
    
    def save_data(self, data, cabecalho):
        table = DataFrame(data[1:], columns=cabecalho)
        table.to_excel(path_processed_data, index=False)

if __name__ == '__main__':
    
    path_processed_data = join(dirname(dirname(dirname(abspath(__file__)))), 'processed_data', '2. Horário de negociação', 
                               'Tabela_horarios_de_negociacao_no_mercado_de_acoes.xlsx')

    extract_and_transform = ExtractAndTransform(path_processed_data)

    table = extract_and_transform.request_page()
    cabecalho = extract_and_transform.get_cabecalho(table)
    data = extract_and_transform.get_data(table)

    cabecalho = extract_and_transform.transform_cabecalho(cabecalho, data)

    extract_and_transform.save_data(data, cabecalho)