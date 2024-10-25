

from pandas import DataFrame
import config
from bs4 import BeautifulSoup

class Transform:

    def __init__(self, path_extracted_data, path_processed_data):
        self.path_extracted_data = path_extracted_data
        self.path_processed_data = path_processed_data

    def read_htm(self):
        """
        Lê um arquivo HTML e retorna um objeto BeautifulSoup.

        Levanta uma exceção se o arquivo não for encontrado ou ocorrer um erro ao ler.
        """
        try:
            with open(self.path_extracted_data, 'r', encoding='utf-8') as file:
                return BeautifulSoup(file.read(), 'html.parser')
        except FileNotFoundError:
            print(f"Erro: O arquivo '{self.path_extracted_data}' não foi encontrado.")
            raise
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            raise

    def get_cabecalho(self, table):
        """
        Extrai os cabeçalhos da tabela e retorna uma lista de textos.

        :param table: Objeto BeautifulSoup representando a tabela.
        :return: Lista de cabeçalhos da tabela.
        """
        return [header.get_text(strip=True) for header in table.find_all('th') if header.get_text(strip=True)]
        

    def get_data(self, table):
        """
        Extrai os dados da tabela, ignorando o cabeçalho, e retorna uma lista de listas.

        :param table: Objeto BeautifulSoup representando a tabela.
        :return: Lista de listas contendo os dados.
        """
        return [
            [col.get_text(strip=True) for col in row.find_all('td')]
            for row in table.find_all('tr')[1:]
            if row.find_all('td')
        ]

    def transform_cabecalho(self, cabecalho, data):
        """
        Transforma os cabeçalhos, duplicando-os conforme necessário e formatando-os com dados.

        :param cabecalho: Lista de cabeçalhos.
        :param data: Lista de listas com os dados.
        :return: Lista transformada de cabeçalhos.
        """
        # Duplicar os headers (em sequência), exceto o primeiro
        duplicated_headers  = [[item] * 2 for item in cabecalho[1:]]

        # Achatar a lista e remover 'After-Market2'
        flattened_list = [item for sublist in duplicated_headers  for item in sublist if item != 'After-Market2']

        # Adicionar o primeiro header de volta
        flattened_list = [cabecalho[0]] + flattened_list

        # Atualizar os últimos 6 cabeçalhos com 'After-Market2'
        lista = [f'After-Market2 {item}' if i >= len(flattened_list) -6 else item 
                 for i, item in enumerate(flattened_list)]
        
        # Formatar os cabeçalhos com dados "INICIO" e "FIM"
        lista2 = [
            item if i == 0 else f'{item} "{data[0][i].upper()}"'
            for i, item in enumerate(lista)
        ]

        return lista2
    
    def save_data(self, data, cabecalho):
        """
        Salva os dados em um arquivo Excel, usando o cabeçalho fornecido.

        :param data: Lista de listas contendo os dados a serem salvos.
        :param cabecalho: Lista com os nomes das colunas.
        """
        if not data or len(data) == 1:
            print("Erro: Não há dados para salvar.")
            return
        
        if len(cabecalho) != len(data[0]):
            print("Erro: O cabeçalho e os dados não têm o mesmo número de colunas.")
            return
        
        try:
            table = DataFrame(data[1:], columns=cabecalho)
            table.to_csv(self.path_processed_data, index=False, encoding='utf-8')
            print(f"Arquivo salvo em: {self.path_processed_data}.")
        except Exception as e:
            print(f"Erro ao salvar os dados: {e}")
    

if __name__ == '__main__':

    transform = Transform(config.path_extracted_data, config.path_processed_data)
    data_htm = transform.read_htm() 
    data = transform.get_data(data_htm)
    cabecalho = transform.transform_cabecalho(transform.get_cabecalho(data_htm), data)
    transform.save_data(data, cabecalho)

    
