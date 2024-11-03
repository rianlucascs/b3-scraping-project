
import config
from os import listdir, remove
from os.path import join, exists
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
)

class Extract:
    """
    Classe para extrair informações de empresas listadas na B3.

    Esta classe utiliza Selenium para acessar páginas da B3, coletando informações relevantes de empresas
    listadas, como nome do pregão, código de negociação, CNPJ, atividade principal, classificação setorial e
    escriturador. Os dados extraídos são salvos em arquivos de texto em um diretório especificado.

    Attributes:
        path_extracted_data (str): Caminho para o diretório onde os dados extraídos serão armazenados.

    Methods:
        ``get_urls(codigo: str) -> str``:
            Obtém a URL correspondente a um código de empresa a partir de um arquivo.

        ``get_element_xpath(driver: webdriver.Chrome, nome: str, xpath: str) -> str``:
            Extrai o texto de um elemento HTML com base no seu XPath.

        ``save_data(path: str, dados, update: bool = False)``:
            Salva os dados extraídos em um arquivo, com opção de atualização.

        ``check_infos()``:
            Verifica a integridade dos dados extraídos, removendo arquivos inválidos.

        ``run(update: bool = False)``:
            Executa o processo de extração de dados das URLs das empresas listadas.
    """
    
    def __init__(self, path_extracted_data: str):
        self.path_extracted_data = path_extracted_data
    
    def get_urls(self, codigo: str) -> str:
        try:
            path_dir_page = join(self.path_extracted_data, codigo, f'url_{codigo}.txt')
            with open(path_dir_page, 'r', encoding='utf-8') as file:
                file = file.read()
                if codigo in file:
                    print(f"Sucesso ao abrir o arquivo: '{codigo}'.")
                    return file
        except OSError as e:
            print(f'Erro ao acessar arquivos em {path_dir_page}: {e}')
            

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
            elemento = WebDriverWait(driver, 0.1).until(
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
    
    def check_infos(self):
        for i, codigo in enumerate(listdir(self.path_extracted_data)):
            path_info = join(self.path_extracted_data, codigo, f'infos_{codigo}.txt')
            with open(path_info, 'r', encoding='utf-8') as file:
                file = file.read()
            if not codigo in file:
                print(f'Informações incorretas: {codigo}, N° {i}')
                print(f'Arquivo deletado: {path_info}.')
                remove(path_info)
            else:
                print(f'Código: {codigo}, Status: OK, N° {i}')
            
            if len(eval(file)) != 7:
                print(f'Quantidade de informações incorretas: {codigo}, N° {i}')
                print(f'Arquivo deletado: {path_info}.')
                remove(path_info)

    def run(self, update=False):
        """
        Executa o processo de extração de dados das URLs.

        Esta função percorre todas as páginas disponíveis, obtém as URLs correspondentes,
        e extrai informações relevantes de cada uma delas usando um navegador controlado pelo Selenium.
        """

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=config.options)

        try:

            for i, codigo in enumerate(listdir(self.path_extracted_data)):
                print(f'Código: {codigo}, N° {i}')
                url = self.get_urls(codigo)
                path_save = join(self.path_extracted_data, codigo, f'infos_{codigo}.txt')
                
                if not exists(path_save) or update:
                    try:

                        driver.get(url) 
                                
                        nome_do_pregao = self.get_element_xpath(
                            driver, 'Nome do Pregão', 
                            '//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[1]/div/div/p[2]'
                            )
                        
                        codigo_de_negociacao = self.get_element_xpath(
                            driver, 'Código de Negociação', 
                            '//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[1]/div/div/p[4]/a'
                            )
                        
                        cnpj = self.get_element_xpath(
                            driver, 'CNPJ', 
                            '//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[1]/div/div/div[2]/p[2]'
                            )
                        atividade_principal = self.get_element_xpath(
                            driver, 'Atividade Principal', 
                            '//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[1]/div/div/div[3]/p[2]'
                            )
                        
                        classificacao_setorial = self.get_element_xpath(
                            driver, 'Classificação Setorial', 
                            '//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[1]/div/div/div[4]/p[2]'
                            )
                        
                        escriturador = self.get_element_xpath(
                            driver, 'Escriturador', 
                            '//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[2]/div/div/p[2]/span[1]'
                            )
                        
                        infos = [codigo, nome_do_pregao, codigo_de_negociacao, cnpj, atividade_principal, 
                                classificacao_setorial, escriturador]
                        
                        self.save_data(path_save, infos, update)

                        print(infos)
                            
                    except WebDriverException as e:
                        print(f"Erro ao acessar a URL {url} ou extrair dados: {e}")
                    except Exception as e:
                        driver.quit()
                        print(f"Erro ao processar as páginas: {e}")
                        print("Tentando reiniciar o processo...")
                        sleep(20)
                        self.run(update=False)

        finally:
            self.check_infos()
            driver.quit() 

if __name__ == '__main__':
    extract = Extract(config.path_extracted_data)
    extract.run()

    