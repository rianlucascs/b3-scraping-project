

import requests
from bs4 import BeautifulSoup
from os.path import exists
import config

class Extract:

    def __init__(self, path_extracted_data):
        self.path_extracted_data = path_extracted_data

    def get_html_page(self, update=True):
        """
        Obtém a página HTML da B3 e salva a tabela em um arquivo.

        Faz uma requisição para o site da B3, extrai a tabela com horários de negociação
        e a salva em um arquivo no caminho especificado. Se o arquivo já existir e
        update for False, a tabela não será sobrescrita.

        Args:
            update (bool): Indica se o arquivo existente deve ser sobrescrito. 
                           O padrão é True.

        """
        url = 'https://www.b3.com.br/pt_br/solucoes/plataformas/puma-trading-system/para-participantes-e-traders/horario-de-negociacao/acoes/'
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', class_='responsive')
            if table is not None:
                if not exists(self.path_extracted_data) or update:
                    with open(self.path_extracted_data, 'w', encoding='utf-8') as file:
                        file.write(str(table))
                    print(f"Tabela salva em: {self.path_extracted_data}")
                else:
                    print(f"A tabela já existe em: {self.path_extracted_data}.")
            else:
                print('Tabela não encontrada na página.')
        except requests.RequestException as e:
            print(f"Erro ao acessar a página: {e}")

if __name__ == '__main__':
    extract = Extract(config.path_extracted_data)
    extract.get_html_page(update=False)