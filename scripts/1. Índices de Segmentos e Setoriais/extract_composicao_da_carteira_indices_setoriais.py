from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import listdir
from time import sleep
import config

__python__ = 3.10

class Extract:
    """
    Classe para extrair dados de índices da B3 e baixar arquivos CSV correspondentes.

    Esta classe é responsável por solicitar a página de cada índice definido e iniciar o download
    do arquivo CSV correspondente, verificando se o arquivo já existe no diretório especificado.

    Attributes:
        path (str): Caminho do diretório onde os arquivos baixados serão salvos.
        indices (list): Lista de índices a serem baixados.

    Methods:
        ``request_page(indice: str) -> None``:
            Solicita a página do índice e inicia o download do arquivo CSV.

        ``check_se_arquivo_existe(indice: str) -> bool``:
            Verifica se o arquivo do índice já existe no diretório de download.

        ``execute() -> None``:
            Executa o loop para baixar os arquivos dos índices, se ainda não existentes.
    """

    def __init__(self, path: str, indices: str = 'IMOB'):
        """
        Inicializa a classe Extract com o caminho para downloads e lista de índices.

        Args:
            path (str): Caminho do diretório onde os arquivos serão baixados.
            indices (list): Lista de índices a serem baixados.
        """
        self.path = path
        self.indices = indices
        print(f"\nDownload: {path}\n")
    
    def request_page(self, indice: str) -> None:
        """
        Solicita a página do índice e inicia o download do arquivo CSV.

        Args:
            indice (str): O índice a ser baixado.
        """
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'download.default_directory': self.path})

        with webdriver.Chrome(options=options) as driver:
            url = f'https://sistemaswebb3-listados.b3.com.br/indexPage/day/{indice}?language=pt-br'
            driver.get(url)

            try:
                download_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, 'Download'))
                )
                download_button.click()
            except Exception as e:
                print(f"Erro ao clicar no botão de download para o índice {indice}: {e}")
            finally:
                sleep(5)  
                print(f'Status: OK\nÍndice: {indice}\nExtensão: CSV\nURL: {url}\n')
    
    def check_se_arquivo_existe(self, indice: str) -> bool:
        """
        Verifica se o arquivo do índice já existe no diretório de download.

        Args:
            indice (str): O índice a ser verificado.

        Returns:
            bool: True se o arquivo existir, False caso contrário.
        """
        for file in listdir(self.path):
            if indice.lower() in file.lower() and file.split('.')[-1] == 'csv':
                print(f'Arquivo existente - composição da carteira: {indice} (arquivo: {file})')
                return True
        return False

    def execute(self) -> None:
        """
        Executa o loop para baixar os arquivos dos índices, se ainda não existentes.
        """
        try:
            for indice in self.indices:
                if not self.check_se_arquivo_existe(indice):
                    self.request_page(indice)
        except Exception as e:
            print(f"Ocorreu um erro durante a execução: {e}")

if __name__ == '__main__':
    carteira_extractor = Extract(config.path_extracted_data, config.INDICES.keys())
    carteira_extractor.execute()





