
import config
from os import listdir
from os.path import join, splitext
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    WebDriverException,
)

class Extract:

    def __init__(self, path_extracted_data):
        self.path_extracted_data = path_extracted_data
        self.dir_page = join(self.path_extracted_data, 'paginas')

    def get_qtd_pages(self) -> int:
        """
        Retorna a quantidade de páginas armazenadas no diretório.

        Esta função conta o número de diretórios presentes no caminho
        especificado por `self.dir_page`, representando as páginas extraídas.

        :return: Número total de páginas.
        """
        return len(listdir(self.dir_page))
    
    def get_urls(self, numero_da_pagina: int) -> Dict[str, str]:
        """
        Obtém as URLs armazenadas em arquivos 'url_{codigo}.txt' em subdiretórios.

        :param numero_da_pagina: O número da página cujos códigos estão sendo verificados.
        :return: Um dicionário onde as chaves são os códigos e os valores são o conteúdo dos arquivos.
        """
        dicionario: Dict[str, str] = {}
        path_dir_page_numero = join(self.dir_page, f'n_page_{numero_da_pagina}')
        try:
            for dir_codigo in [item for item in listdir(path_dir_page_numero) if splitext(item)[1] == '']:
                path_file = join(path_dir_page_numero, dir_codigo, f'url_{dir_codigo}.txt')
                with open(path_file, 'r', encoding='utf-8') as file:
                    dicionario[dir_codigo] = file.read()
                print(f"Sucesso ao abrir o arquivo: '{dir_codigo}'.")
                return dicionario
        except OSError as e:
            print(f'Erro ao acessar arquivos em {path_file}: {e}')

    def get_element_xpath(self, driver: webdriver.Chrome, nome: str, xpath: str) -> None:
        try:
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return elemento.text
        except NoSuchElementException:
            print(f"Erro: O elemento '{nome}' não foi encontrado.")
            return ""
        except WebDriverException as e:
            print(f"Erro ao interagir com o WebDriver: {e}")
            return ""
            
    def run(self):
        
        for numero_da_pagina in range(1, self.get_qtd_pages() + 1):
            dict_urls = self.get_urls(numero_da_pagina)
            
            for codigo, url in dict_urls.items():
                options = webdriver.ChromeOptions()

                with webdriver.Chrome(options=options) as driver:
                    driver.get(url)
                    
                    nome_do_pregao = self.get_element_xpath(driver, 'Nome do Pregão', '//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[1]/div/div/p[2]')
                    codigo_de_negciacao = self.get_element_xpath(driver, 'Código de Negociação', '//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[1]/div/div/p[4]/a')

                    print(nome_do_pregao, codigo_de_negciacao)



if __name__ == '__main__':

    extract = Extract(config.path_extracted_data)
    extract.run()

    