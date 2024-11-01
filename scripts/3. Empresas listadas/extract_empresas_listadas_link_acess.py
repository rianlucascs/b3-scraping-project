from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from os.path import join, exists, splitext
from os import makedirs, listdir, remove
import config
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    WebDriverException,
)
from typing import Dict, List

__python__ = 3.10

class Extract:
    """
    Classe para extrair informações de empresas listadas na B3.

    Esta classe utiliza o Selenium para interagir com a interface web da B3,
    permitindo a extração de códigos de ações, salvamento de URLs, e organização
    dos dados em diretórios específicos. As operações incluem navegação por páginas,
    verificação da existência de arquivos e diretórios, e salvamento de informações
    em arquivos CSV e TXT.

    Attributes:
        path_extracted_data (str): Caminho para o diretório onde os dados extraídos serão salvos.

    Methods:
        run(): Inicia o processo de extração de informações da B3.
    """
    def __init__(self, path_extracted_data: str):
        self.path_extracted_data = path_extracted_data
    
    def get_codigos_page(self, driver: webdriver.Chrome) -> List[str]:
        """
        Extrai códigos de empresas listadas na página atual.

        Esta função localiza todos os elementos com a classe 'card-title2'
        e retorna uma lista de textos únicos contidos nesses elementos.

        :param driver: Instância do WebDriver para interação com a página.
        :return: Lista de códigos extraídos, sem duplicatas.
        """
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-title2'))
            )
            rows = driver.find_elements(By.CLASS_NAME, 'card-title2')
            return list({row.text for row in rows})
        except NoSuchElementException:
            print("Nenhum elemento encontrado com a classe 'card-title2'.")
            return []
        except WebDriverException as e:
            print(f"Erro ao interagir com o WebDriver: {e}.")
            return []

    def get_quantidade_de_paginas(self, driver:webdriver.Chrome):
        """
        Extrai códigos de empresas listadas na página atual.

        Esta função localiza todos os elementos com a classe 'card-title2'
        e retorna uma lista de textos únicos contidos nesses elementos.

        :param driver: Instância do WebDriver para interação com a página.
        :return: Lista de códigos extraídos, sem duplicatas.
        :raises NoSuchElementException: Se nenhum elemento com a classe 'card-title2' for encontrado.
        :raises WebDriverException: Se ocorrer um erro durante a interação com o WebDriver.
        """
        try:
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="listing_pagination"]/pagination-template/ul/li[9]/a/span[2]'))
            )
            return int(elemento.text)
        except NoSuchElementException:
            print("O elemento que contém a quantidade de páginas não foi encontrado.")
            raise
        except ValueError:
            print("O texto encontrado não pode ser convertido para um inteiro.")
            raise

    def get_codigo_page(self, driver: webdriver.Chrome, n_item: int) -> str:
        """
        Extrai o texto do código na página com base na posição do item.

        Esta função localiza um elemento com base no índice fornecido e retorna
        seu texto. O índice deve corresponder à posição do elemento dentro do
        contêiner de navegação.

        :param driver: Instância do WebDriver para interação com a página.
        :param n_item: Índice do item a ser extraído (baseado em 1).
        :return: Texto do elemento encontrado.
        :raises NoSuchElementException: Se o elemento especificado não for encontrado.
        :raises WebDriverException: Se ocorrer um erro durante a interação com o WebDriver.
        """
        try:
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="nav-bloco"]/div/div[{n_item}]/div/div/h5'))
            )
            return elemento.text
        except NoSuchElementException:
            print(f"Elemento na posição {n_item} não encontrado.")
            return ""
        except WebDriverException as e:
            print(f"Erro ao interagir com o WebDriver: {e}")
            return ""

    def get_xpath_numero_pagina(self, driver: webdriver.Chrome) -> int:
        """
        Extrai o número da página atual a partir do elemento com a classe 'current'.

        Esta função localiza o elemento que indica a página atual e retorna o
        número da página. O número é extraído da segunda linha do texto do elemento.

        :param driver: Instância do WebDriver para interação com a página.
        :return: Número da página atual como um inteiro.
        :raises NoSuchElementException: Se o elemento com a classe 'current' não for encontrado.
        :raises ValueError: Se o texto do elemento não puder ser convertido em inteiro.
        :raises WebDriverException: Se ocorrer um erro durante a interação com o WebDriver.
        """
        try:
            xpath_numero_page = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'current'))
            )
            return int(xpath_numero_page.text.split('\n')[1])
        except NoSuchElementException:
            print("Elemento com a classe 'current' não encontrado.")
            raise
        except (ValueError, IndexError):
            print("Erro ao converter o texto do elemento para um número.")
            raise
        except WebDriverException as e:
            print(f"Erro ao interagir com o WebDriver: {e}")
            raise

    def acess_page_codigo(self, driver: webdriver.Chrome, n_item: int) -> None:
        """
        Acessa a página de um código específico.

        Esta função espera até que o elemento correspondente ao código especificado esteja clicável
        e, em seguida, clica nele.

        :param driver: Instância do WebDriver para interagir com o navegador.
        :param n_item: O índice do item que será clicado.
        :raises TimeoutException: Se o elemento não estiver clicável dentro do tempo limite.
        :raises WebDriverException: Se houver um erro ao tentar clicar no elemento.
        """
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[@id="nav-bloco"]/div/div[{n_item}]/div/div'))
            )
            element.click()
        except TimeoutException:
            print(f'Tempo esgotado: o elemento no item {n_item} não ficou clicável.')
        except WebDriverException as e:
            print(f'Erro ao tentar clicar no elemento do item {n_item}: {e}')        

    def next_page(self, driver:webdriver.Chrome) -> None:
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
        
    def adjust_numero_pagina(self, driver: webdriver.Chrome, numero_pagina_loop: int) -> bool:
        """
        Ajusta a página atual do driver até que o número da página corresponda ao esperado.

        Esta função verifica continuamente o número da página exibido e navega para a próxima página
        até que o número atual seja igual ao número esperado.

        :param driver: Instância do WebDriver para interagir com o navegador.
        :param numero_pagina_loop: O número da página esperado.
        :return: True se o número da página atual corresponder ao número esperado, False caso contrário.
        """
        xpath_numero_pagina = self.get_xpath_numero_pagina(driver)
        if xpath_numero_pagina == numero_pagina_loop:
            return True
        
        sleep(0.2)
        while True:
            xpath_numero_pagina = self.get_xpath_numero_pagina(driver)
            sleep(0.1)
            
            if xpath_numero_pagina == numero_pagina_loop:
                sleep(1)
                return True
            
            self.next_page(driver)
        
    def save_file(self, path: str, content: str, update: bool = False) -> None:
        """
        Salva o conteúdo em um arquivo no caminho especificado.

        Esta função verifica se o arquivo já existe. Se não existir ou se
        o parâmetro `update` for True, o conteúdo será salvo. Caso contrário,
        uma mensagem informando que o arquivo já existe será exibida.

        :param path: Caminho do arquivo onde o conteúdo será salvo.
        :param content: O conteúdo a ser salvo no arquivo.
        :param update: Se True, o arquivo existente será sobrescrito.
        :raises OSError: Se ocorrer um erro ao tentar salvar o arquivo.
        """
        if not exists(path) or update:
            try:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(str(content))
                print(f"Informações salvas em: {path}")
            except OSError as e:
                print(f'Erro ao salvar o arquivo: {e}')
        else:
            print(f'O arquivo já existe: {path}')

    def check_urls_arquivos(self, path_dir_page: str, numero_da_pagina: int) -> bool:
        try:
            list_files_dir = [item for item in listdir(path_dir_page) if splitext(item)[1] == '']
            dicionario: Dict[str, bool] = {}

            for indice in list_files_dir:
                file_path = join(path_dir_page, indice, f'url_{indice}.txt')
                with open(file_path, 'r', encoding='utf-8') as file:
                    conteudo = file.read()
                    dicionario[indice] = indice in conteudo
    
        except OSError as e:
            print(f'Erro ao acessar arquivos em {path_dir_page}: {e}')
            return False
    
    def run(self):
        """
        Extrai informações de empresas listadas na B3 a partir da interface web.

        Este método inicializa um navegador Chrome, acessa a página de listagem de empresas e itera
        através de todas as páginas disponíveis. Para cada página, ele extrai códigos de empresas,
        salva-os em arquivos e verifica a existência de diretórios correspondentes. Além disso, 
        acessa páginas específicas para cada código, salvando as URLs.

        O fluxo do processo é o seguinte:
        1. Acessa a URL da lista de empresas.
        2. Obtém o total de páginas disponíveis.
        3. Para cada página, ajusta o número da página no navegador, extrai os códigos e os salva.
        4. Para cada código extraído, acessa a página correspondente, salva a URL e volta para a lista.
        5. Realiza verificações para assegurar que os diretórios e URLs estão corretos.

        :raises Exception: Levanta exceções gerais em caso de falhas durante a interação com o navegador 
                        ou ao acessar elementos na página.
        """
        try:
            options = webdriver.ChromeOptions()
            with webdriver.Chrome(options=options) as driver:
                driver.get(config.url)
                total_paginas = self.get_quantidade_de_paginas(driver)
                print(f'Número de páginas total: {total_paginas}')
                
                count_data = 0
                for numero_da_pagina in range(1, total_paginas + 1):
                    self.adjust_numero_pagina(driver, numero_da_pagina)
                    print(f'Número da página: {numero_da_pagina}')

                    lista_codigos = self.get_codigos_page(driver)

                    sleep(3)

                    for n_item in range(1, len(lista_codigos) + 1):
                        count_data += 1
                        self.adjust_numero_pagina(driver, numero_da_pagina)
                        codigo = self.get_codigo_page(driver, n_item)
                        print(f'Página {numero_da_pagina}, Item: {n_item}, Código: {codigo}, N°: {count_data}')

                        path_dir_codigo = join(self.path_extracted_data, codigo)
                        if not exists(path_dir_codigo):
                            makedirs(path_dir_codigo)
                        
                        if not exists(path_dir_codigo) or not exists(join(path_dir_codigo, f'url_{codigo}.txt')):
                            sleep(3)
                            self.acess_page_codigo(driver, n_item)
                            sleep(3)
                            self.save_file(join(self.path_extracted_data, f'url_{codigo}.txt'), driver.current_url, update=False)
                            sleep(3)
                            driver.back()
                            sleep(2)
                    
                    # self.check_urls_arquivos(path_dir_page, numero_da_pagina)

        except Exception as e:
            
            # Tem que tirar a criação de diretórios por página;
            # Pois está travando e causando erros desenecessários 
            print(f"Erro ao processar as páginas: {e}")
            print("Tentando reiniciar o processo...")
            sleep(40)
            self.run()

            
if __name__ == '__main__':
    
    extract = Extract(config.path_extracted_data)
    extract.run()
