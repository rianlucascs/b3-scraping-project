from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
from os.path import join, exists
from os import makedirs
import config
from typing import Optional
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException


class Extract:

    def __init__(self, path_extracted_data):
        self.path_extracted_data = path_extracted_data
        self.n_item = 0 
        self.n_page = 1
        pass
    
    def get_and_save_codigos_page(self, driver:webdriver.Chrome, path, update=False) -> list:
        """
        Extrai códigos de seleção da B3.

        :param driver: Instância do WebDriver (ex: webdriver.Chrome).
        :param path: Caminho para o diretório onde o arquivo será salvo.
        :param update: Se True, o arquivo existente será atualizado. Caso contrário, será ignorado se já existir.
        :return: Lista de códigos extraídos, sem duplicatas.
        """
        rows = driver.find_elements(By.CLASS_NAME, 'card-title2')
        lista = list(set([row.text for row in rows]))
        path_file = join(path, 'Códigos_page.txt')
        if not exists(path_file) or update:
            try:
                with open(path_file, 'w', encoding='utf-8') as file:
                    file.write(str(lista))
                print(f"Informações salvas em: {path_file}")
            except OSError as e:
                print(f'Erro ao salvar arquivo: {e}')
        else:
            print(f"Arquivo já existe: {path_file}. Ignorando a gravação.")
        return lista

    def get_quantidade_de_paginas(self, driver:webdriver.Chrome):
        """
        Obtém a quantidade total de páginas de resultados na B3.

        Esta função localiza o elemento que contém o número total de páginas
        e retorna esse valor como um inteiro.

        :param driver: Instância do WebDriver (ex: webdriver.Chrome).
        :return: Número total de páginas como um inteiro.
        :raises NoSuchElementException: Se o elemento não for encontrado.
        :raises ValueError: Se o texto não puder ser convertido para um inteiro.
        """
        try:
            quantidade_texto = driver.find_element(By.XPATH, '//*[@id="listing_pagination"]/pagination-template/ul/li[9]/a/span[2]').text
            return int(quantidade_texto)
        except NoSuchElementException:
            print("O elemento que contém a quantidade de páginas não foi encontrado.")
            raise
        except ValueError:
            print("O texto encontrado não pode ser convertido para um inteiro.")
            raise

    def save_url_and_create_dir_codigo(self, url, codigo, path, update=False) -> None:
        """
        Salva uma URL em um arquivo e cria um diretório com o código.

        Esta função verifica se o diretório correspondente ao código já existe. 
        Se não existir, ele será criado. Em seguida, salva a URL em um arquivo 
        chamado 'url.txt'. Se o arquivo já existir e o parâmetro `update` for False, 
        a gravação será ignorada.

        :param url: A URL a ser salva.
        :param codigo: O código usado para criar o diretório.
        :param path: Caminho para o diretório onde o novo diretório será criado.
        :param update: Se True, o arquivo existente será atualizado.
        """

        new_dir = join(path, codigo)
        if not exists(new_dir):
            makedirs(new_dir)
        path_file = join(new_dir, f'url_{codigo}.txt')
        if not exists(path_file) or update:
            try:
                with open(path_file, 'w', encoding='utf-8') as file:
                    file.write(url)
            except OSError as e:
                print(f'Erro ao salvar o arquivo: {e}')
        else:
            print(f'O arquivo já existe: {path_file}')

    def next_page(self, driver:webdriver.Chrome):
        """
        Clica na próxima página nos resultados da B3.

        Esta função espera que o botão de próxima página esteja clicável e,
        em seguida, realiza o clique. Se o botão não estiver disponível, 
        será levantada uma exceção.

        :param driver: Instância do WebDriver (ex: webdriver.Chrome).
        :raises TimeoutException: Se o botão de próxima página não se tornar clicável dentro do tempo limite.
        :raises ElementClickInterceptedException: Se o clique no botão for interceptado por outro elemento.
        """
        try:
            next_page = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="listing_pagination"]/pagination-template/ul/li[10]/a'))
            )
            next_page.click()
        except TimeoutException:
            print("O botão de próxima página não se tornou clicável dentro do tempo limite.")
        except ElementClickInterceptedException:
            print("O clique no botão de próxima página foi interceptado por outro elemento.")


    def save_all_codigos(self, path, codigo):
        with open(join(path, 'all_Códigos'), 'a', encoding='utf-8') as file:
            file.write(f'{codigo} ')

    def check_codigo(self, path, codigo):
        if not exists(join(path, 'all_Códigos')):
            return False
        with open(join(path, 'all_Códigos'), 'r', encoding='utf-8') as file:
            if codigo in file.read():
                return True
            return False

    def driver_page(self):
        url = 'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/search?language=pt-br'

        options = webdriver.ChromeOptions()

        with webdriver.Chrome(options=options) as driver:
            driver.get(url)
            qtd_paginas = self.get_quantidade_de_paginas(driver)
            for n_page in list(range(1, qtd_paginas + 1)): # Loop paginas

                print(f'n_page: {n_page}')

                new_dir = join(self.path_extracted_data, 'paginas', f'n_page_{n_page}')

                if not exists(new_dir):
                    makedirs(new_dir)

                sleep(3)

                codigos_page = self.get_and_save_codigos_page(driver, new_dir, update=True)
                
                self.n_item = 0
                while self.n_item <= len(codigos_page)-1: # Loop itemns da pagina
                    self.n_item += 1
                    
                    if self.n_item == len(codigos_page):
                        self.n_page += 1

                    n_item = self.n_item
                    
                    print(f'n_item: {n_item}')
                    
                    codigo = driver.find_element(By.XPATH, f'//*[@id="nav-bloco"]/div/div[{n_item}]/div/div/h5').text
                    # Xpath que indica a pagina
                    # //*[@id="listing_pagination"]/pagination-template/ul/li[2]
                    # //*[@id="listing_pagination"]/pagination-template/ul/li[2]
                    if not codigo in codigos_page:
                        self.next_page(driver)
                        sleep(3)
                        self.n_item = self.n_item - 1

                        

                    if not self.check_codigo(join(self.path_extracted_data, 'paginas'), codigo):

                        element = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f'//*[@id="nav-bloco"]/div/div[{n_item}]/div/div')))    
                        element.click() 

                        sleep(3)

                        url = driver.current_url
                        
                        self.save_url_and_create_dir_codigo(url, codigo, new_dir, update=True)

                        sleep(3)

                        self.save_all_codigos(join(self.path_extracted_data, 'paginas'), codigo)
                        driver.back()


                        
                
                
                

                
            

if __name__ == '__main__':
    
    extract = Extract(config.path_extracted_data)
    extract.driver_page()
