
import config
from os import listdir
from os.path import join, splitext, exists
from typing import Dict
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
)

class Extract:
    """
    Classe responsável por extrair dados de páginas da web.

    Esta classe gerencia a leitura de URLs de arquivos, a navegação por páginas da web 
    utilizando Selenium e a extração de informações relevantes. Além disso, realiza a 
    contagem de páginas disponíveis e o armazenamento de dados extraídos em arquivos 
    específicos.

    Atributos:
        path_extracted_data (str): Caminho para o diretório onde os dados extraídos são armazenados.
        dir_page (str): Caminho para o diretório das páginas extraídas.
    """
    def __init__(self, path_extracted_data: str):
        self.path_extracted_data = path_extracted_data
        self.dir_page = join(self.path_extracted_data, 'paginas')

    def get_qtd_pages(self) -> int:
        """
        Conta o número de páginas armazenadas no diretório.

        Esta função verifica a quantidade de diretórios presentes em `self.dir_page`,
        que representam as páginas extraídas.

        :return: O número total de páginas disponíveis.
        """
        qtd_pages = len(listdir(self.dir_page))
        print(f"Quantidade de paginas disponíveis: {qtd_pages}")
        return qtd_pages
    
    def get_urls(self, numero_da_pagina: int) -> Dict[str, str]:
        """
        Obtém as URLs armazenadas em arquivos 'url_{codigo}.txt' dentro de subdiretórios.

        Esta função lê os arquivos correspondentes a uma página específica e
        armazena as URLs em um dicionário.

        :param numero_da_pagina: O número da página cujos URLs estão sendo recuperados.
        :return: Um dicionário onde as chaves são os códigos dos diretórios e os valores são o conteúdo dos arquivos de URL.
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
            self.save_data(join(path_dir_page_numero, 'erro_CHECK_URLs_2.txt'), dir_codigo)
            return {}

    def get_element_xpath(self, driver: webdriver.Chrome, nome: str, xpath: str) -> str:
        """
        Obtém o texto de um elemento da página usando seu XPath.

        Esta função espera até que o elemento esteja presente na página e retorna seu texto.

        :param driver: Instância do webdriver utilizada para a navegação.
        :param nome: Nome do elemento, utilizado para mensagens de log.
        :param xpath: XPath do elemento a ser localizado.
        :return: O texto do elemento se encontrado; caso contrário, uma string vazia.
        """
        try:
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return elemento.text
        except NoSuchElementException:
            print(f"Erro: O elemento '{nome}' não foi encontrado.")
            return ""
        except WebDriverException as e:
            print(f"Erro ao interagir com o WebDriver '{nome}'")
            return ""
        
    def save_data(self, path: str, dados, update: bool = False):
        """
        Salva dados em um arquivo, se não existir ou se a atualização for permitida.

        Esta função grava os dados fornecidos no caminho especificado. Se o arquivo já existir,
        a gravação só ocorre se o parâmetro `update` for definido como True.

        :param path: Caminho do arquivo onde os dados serão salvos.
        :param dados: Dados a serem salvos no arquivo.
        :param update: Indica se o arquivo existente deve ser atualizado.
        """
        if not exists(path) or update:
            try:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(str(dados))
                print(f"Informações salvas em: {path}")
            except OSError as e:
                print(f'Erro ao salvar o arquivo: {e}')
        else:
            print(f'O arquivo já existe: {path}')

    def run(self):
        """
        Executa o processo de extração de dados das URLs.

        Esta função percorre todas as páginas disponíveis, obtém as URLs correspondentes,
        e extrai informações relevantes de cada uma delas usando um navegador controlado pelo Selenium.
        """
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)

        try:

            for numero_da_pagina in range(1, self.get_qtd_pages() + 1):
                print(f'* Número da Página: {numero_da_pagina}')
                dict_urls = self.get_urls(numero_da_pagina)
                if dict_urls != {}:
                    for codigo, url in dict_urls.items():
                        path_save = join(self.dir_page, f'n_page_{numero_da_pagina}', codigo, f'infos_{codigo}.txt')
                        if not exists(path_save):
                            try:
                                driver.get(url) 
                                
                                nome_do_pregao = self.get_element_xpath(driver, 'Nome do Pregão', '//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[1]/div/div/p[2]')
                                codigo_de_negociacao = self.get_element_xpath(driver, 'Código de Negociação', '//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[1]/div/div/p[4]/a')
                                cnpj = self.get_element_xpath(driver, 'CNPJ', '//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[1]/div/div/div[2]/p[2]')
                                atividade_principal = self.get_element_xpath(driver, 'Atividade Principal', '//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[1]/div/div/div[3]/p[2]')
                                classificacao_setorial = self.get_element_xpath(driver, 'Classificação Setorial', '//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[1]/div/div/div[4]/p[2]')
                                escriturador = self.get_element_xpath(driver, 'Escriturador', '//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[2]/div/div/p[2]/span[1]')
                                
                                
                                self.save_data(path_save, [numero_da_pagina, codigo, nome_do_pregao, codigo_de_negociacao, cnpj, 
                                                        atividade_principal, classificacao_setorial, escriturador])
                            
                            except WebDriverException as e:
                                print(f"Erro ao acessar a URL {url} ou extrair dados: {e}")
                            except Exception as e:
                                driver.quit()
                                print(f"Erro ao processar as páginas: {e}")
                                print("Tentando reiniciar o processo...")
                                sleep(20)
                                self.run()

        finally:
            driver.quit() 

if __name__ == '__main__':
    extract = Extract(config.path_extracted_data)
    extract.run()

    