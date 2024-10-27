from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from os.path import join, exists, splitext
from os import makedirs, listdir
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
        dir_page (str): Caminho para o diretório que armazena as páginas extraídas.

    Methods:
        run(): Inicia o processo de extração de informações da B3.
    """
    def __init__(self, path_extracted_data):
        self.path_extracted_data = path_extracted_data
        self.dir_page = join(self.path_extracted_data, 'paginas')
    
    def get_codigos_page(self, driver: webdriver.Chrome) -> List[str]:
        """
        Extrai códigos de empresas listadas na página atual.

        Esta função localiza todos os elementos com a classe 'card-title2'
        e retorna uma lista de textos únicos contidos nesses elementos.

        :param driver: Instância do WebDriver para interação com a página.
        :return: Lista de códigos extraídos, sem duplicatas.
        """
        try:
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
            quantidade_texto = driver.find_element(By.XPATH, '//*[@id="listing_pagination"]/pagination-template/ul/li[9]/a/span[2]').text
            return int(quantidade_texto)
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
            return driver.find_element(By.XPATH, f'//*[@id="nav-bloco"]/div/div[{n_item}]/div/div/h5').text
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
            xpath_numero_page = driver.find_element(By.CLASS_NAME, f'current')
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

    def save_url_codigo(self, url: str, codigo: str, path: str, update: bool = False) -> None:
        """
        Salva uma URL em um arquivo.

        A URL será salva em um arquivo nomeado 'url_{codigo}.txt'. Se o arquivo já existir
        e o parâmetro `update` for False, a gravação será ignorada.

        :param url: A URL a ser salva.
        :param codigo: O código usado para nomear o arquivo.
        :param path: Caminho para o diretório onde o arquivo será salvo.
        :param update: Se True, o arquivo existente será sobrescrito. O padrão é False.
        :raises OSError: Se ocorrer um erro ao salvar o arquivo.
        """
        path_file = join(path, f'url_{codigo}.txt')
        try:
            self.save_file(path_file, url, update=update)
            print(f"URL salva em: {path_file}")
        except OSError as e:
            print(f'Erro ao salvar o arquivo: {e}')
    
    def save_list_codigo(self, lista_codigos: List[str], numero_da_pagina: int, path: str, update: bool=False) -> None:
        """
        Salva uma lista de códigos em um arquivo.

        A lista de códigos será salva em um arquivo nomeado 'Códigos_n_page_{numero_da_pagina}.txt'.
        Se o arquivo já existir e o parâmetro `update` for False, a gravação será ignorada.

        :param lista_codigos: Lista de códigos a serem salvos.
        :param numero_da_pagina: Número da página associado à lista de códigos.
        :param path: Caminho para o diretório onde o arquivo será salvo.
        :param update: Se True, o arquivo existente será sobrescrito. O padrão é False.
        :raises OSError: Se ocorrer um erro ao salvar o arquivo.
        """
        path_file = join(path, f'Códigos_n_page_{numero_da_pagina}.txt')
        try:
            self.save_file(path_file, lista_codigos, update=update)
            print(f"Lista código salva em: {path_file}")
        except OSError as e:
            print(f'Erro ao salvar o arquivo: {e}')

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

    def create_dir_numero_pagina(self, numero_da_pagina: int) -> str:
        """
        Cria um diretório para a página especificada.

        :param numero_da_pagina: O número da página para a qual o diretório será criado.
        :return: O caminho do diretório criado ou existente.
        :raises OSError: Se ocorrer um erro ao criar o diretório.
        """
        path = join(self.dir_page, f'n_page_{numero_da_pagina}')
        try:
            if not exists(path):
                makedirs(path)
            return path
        except OSError as e:
            print(f"Erro ao criar o diretório para a página {numero_da_pagina}: {e}")
            return ""
        
    def create_dir_codigo(self, numero_da_pagina: int, codigo: str) -> str:
        """
        Cria um diretório para um código específico na página especificada.

        :param numero_da_pagina: O número da página onde o diretório será criado.
        :param codigo: O código usado para nomear o diretório.
        :return: O caminho do diretório criado ou existente.
        :raises OSError: Se ocorrer um erro ao criar o diretório.
        """
        path = join(self.dir_page, f'n_page_{numero_da_pagina}', codigo)
        try:
            if not exists(path):
                makedirs(path)
            return path
        except OSError as e:
            print(f'Erro ao criar o diretório para o código {codigo} na página {numero_da_pagina}: {e}')
            return ""
        
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
        
        sleep(0.3)
        while True:
            xpath_numero_pagina = self.get_xpath_numero_pagina(driver)
            sleep(0.1)
            
            if xpath_numero_pagina == numero_pagina_loop:
                return True
            
            self.next_page(driver)

    def check_dirs_codigos(self, lista_codigos: List[str], path_dir_page: str, numero_da_pagina: int) -> bool:
        """
        Verifica se todos os diretórios em um caminho específico estão presentes em uma lista de códigos.

        Esta função lista os diretórios no caminho especificado e checa se todos os nomes
        desses diretórios estão contidos na lista de códigos fornecida.

        :param lista_codigos: Lista de códigos a serem verificados.
        :param path_dir_page: Caminho do diretório onde os diretórios serão verificados.
        :param numero_da_pagina: O número da página atual.
        """
        try:
            # Lista os diretórios no caminho especificado
            list_files_dir = [item for item in listdir(path_dir_page) if splitext(item)[1] == '']
            # Verifica se todos os diretórios estão na lista de códigos
            if all(item in lista_codigos for item in list_files_dir):
                print(f'Diretórios dos códigos criados corretamente, Página: {numero_da_pagina}')
            else:
                print(f'Alguns diretórios dos códigos não foram criados corretamente na Página: {numero_da_pagina}')
                self.save_file(join(path_dir_page, 'erro_CHECK_DIRs.txt'), content=[list_files_dir, lista_codigos])

        except OSError as e:
            print(f'Erro ao acessar o diretório {path_dir_page}: {e}')
            
    
    def check_urls_arquivos(self, path_dir_page: str, numero_da_pagina: int) -> bool:
        """
        Verifica se todos os arquivos 'url_{indice}.txt' em diretórios especificados contêm o nome do diretório.

        Esta função lista os diretórios em um caminho específico, abre o arquivo 'url_{indice}.txt'
        em cada um deles e verifica se o nome do diretório está contido nesse arquivo.

        :param path_dir_page: Caminho do diretório onde os subdiretórios estão localizados.
        :param numero_da_pagina: O número da página atual.
        :raises OSError: Se ocorrer um erro ao acessar diretórios ou arquivos.
        """
        try:
            list_files_dir = [item for item in listdir(path_dir_page) if splitext(item)[1] == '']
            dicionario: Dict[str, bool] = {}

            for indice in list_files_dir:
                file_path = join(path_dir_page, indice, f'url_{indice}.txt')
                with open(file_path, 'r', encoding='utf-8') as file:
                    conteudo = file.read()
                    dicionario[indice] = indice in conteudo
        
            if all(dicionario.values()):
                print(f'URLs criadas corretamente.')
            else:
                print(f'Algumas URLs não foram criados corretamente na Página: {numero_da_pagina}.')
                self.save_file(join(path_dir_page, 'erro_CHECK_URLs.txt'), content=dicionario)

        except OSError as e:
            print(f'Erro ao acessar arquivos em {path_dir_page}: {e}')
    
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
        
        options = webdriver.ChromeOptions()
        with webdriver.Chrome(options=options) as driver:
            driver.get(config.url)
            total_paginas = self.get_quantidade_de_paginas(driver)
            
            for numero_da_pagina in range(1, total_paginas + 1):
                self.adjust_numero_pagina(driver, numero_da_pagina)
                print(f'Número da página: {numero_da_pagina}')
                path_dir_page = self.create_dir_numero_pagina(numero_da_pagina)
                lista_codigos = self.get_codigos_page(driver)
                self.save_list_codigo(lista_codigos, numero_da_pagina, path_dir_page, update=False)
                sleep(3)

                for n_item in range(1, len(lista_codigos) + 1):
                    self.adjust_numero_pagina(driver, numero_da_pagina)
                    codigo = self.get_codigo_page(driver, n_item)
                    print(f'Página {numero_da_pagina}, Item: {n_item}, Código: {codigo}')
                    
                    if not exists(join(path_dir_page, codigo)):
                        sleep(3)
                        self.acess_page_codigo(driver, n_item)
                        sleep(3)
                        path_dir_codigo = self.create_dir_codigo(numero_da_pagina, codigo)
                        self.save_url_codigo(driver.current_url, codigo, path_dir_codigo, update=True)
                        sleep(3)
                        driver.back()
                        sleep(2)
                
                self.check_dirs_codigos(lista_codigos, path_dir_page, numero_da_pagina)

                self.check_urls_arquivos(path_dir_page, numero_da_pagina)
            
if __name__ == '__main__':
    
    extract = Extract(config.path_extracted_data)
    extract.run()
