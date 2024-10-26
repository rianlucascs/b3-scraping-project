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
        self.dir_page = join(self.path_extracted_data, 'paginas')
        self.n_item = 0 
        self.n_page = 1
        pass
    
    def get_codigos_page(self, driver:webdriver.Chrome) -> list:
        rows = driver.find_elements(By.CLASS_NAME, 'card-title2')
        lista = list(set([row.text for row in rows]))
        # path_file = join(path, 'Códigos_page.txt')
        return lista
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

    def save_url_codigo(self, url, codigo, path, update=False) -> None:
        """
        Salva uma URL em um arquivo e cria um diretório com o código.

        Salva a URL em um arquivo chamado 'url.txt'. Se o arquivo já existir e o parâmetro 
        `update` for False, a gravação será ignorada.

        :param url: A URL a ser salva.
        :param codigo: O código usado para criar o diretório.
        :param path: Caminho para o diretório onde o novo diretório será criado.
        :param update: Se True, o arquivo existente será atualizado.
        """
        path_file = join(path, f'url_{codigo}.txt')
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

    def get_xpath_numero_pagina(self, driver):
        xpath_numero_page = driver.find_element(By.CLASS_NAME, f'current')
        return int(xpath_numero_page.text.split('\n')[1])

    #
    def create_dir_numero_pagina(self, numero_da_pagina):
        path = join(self.dir_page, f'n_page_{numero_da_pagina}')
        if not exists(path):
            makedirs(path)
        return path
    
    def create_dir_codigo(self, numero_da_pagina, codigo):
        path = join(self.dir_page, f'n_page_{numero_da_pagina}', codigo)
        if not exists(path):
            makedirs(path)
        return path
    
    def adjust_numero_pagina(self, driver, numero_pagina_loop):
        xpath_numero_pagina = self.get_xpath_numero_pagina(driver)
        if xpath_numero_pagina == numero_pagina_loop:
            return True
        sleep(0.3)
        while True:
            xpath_numero_pagina = self.get_xpath_numero_pagina(driver)
            sleep(0.3)
            if xpath_numero_pagina == numero_pagina_loop:
                return True
            self.next_page(driver)

    def get_codigo_page(self, driver, n_item):
        return driver.find_element(By.XPATH, f'//*[@id="nav-bloco"]/div/div[{n_item}]/div/div/h5').text

    def acess_page_codigo(self, driver, n_item):
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="nav-bloco"]/div/div[{n_item}]/div/div')))    
        element.click() 

    def driver_page_2(self):
        url = 'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/search?language=pt-br'
        
        options = webdriver.ChromeOptions()
        with webdriver.Chrome(options=options) as driver:
            driver.get(url)
            total_paginas = self.get_quantidade_de_paginas(driver)
            
            for numero_da_pagina in list(range(1, total_paginas + 1)):
                self.adjust_numero_pagina(driver, numero_da_pagina)
                print(f'Número da pagina {numero_da_pagina}')
                path_dir_page = self.create_dir_numero_pagina(numero_da_pagina)
                list_codigos = self.get_codigos_page(driver)
                sleep(3)
                print(list_codigos)

                for n_item in list(range(1, len(list_codigos) + 1)):
                    self.adjust_numero_pagina(driver, numero_da_pagina)
                    codigo = self.get_codigo_page(driver, n_item)
                    print(f'Número da pagina {numero_da_pagina} Numero item: {n_item}, Código {codigo}')
                    
                    if not exists(join(path_dir_page, codigo)):
                        sleep(3)
                        self.acess_page_codigo(driver, n_item)
                        sleep(3)
                        path_dir_codigo = self.create_dir_codigo(numero_da_pagina, codigo)
                        self.save_url_codigo(driver.current_url, codigo, path_dir_codigo, update=True)
                        sleep(3)
                        driver.back()
                        sleep(3)


                        
            

if __name__ == '__main__':
    
    extract = Extract(config.path_extracted_data)
    extract.driver_page_2()
