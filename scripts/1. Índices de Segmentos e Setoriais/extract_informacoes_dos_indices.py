import requests
from bs4 import BeautifulSoup
from os.path import join, exists
import config

class Extract:

    def __init__(self, path, indices):
        """
        Inicializa a classe Extract com o caminho do diretório e a lista de índices.

        Args:
            path (str): Caminho do diretório para salvar os arquivos.
            indices (list): Lista de índices a serem extraídos.
        """
        self.path = path
        self.indices = indices

    def get_link(self):
        """
        Obtém links para páginas de detalhes dos índices na B3.

        Returns:
            list: Lista de URLs dos índices.
        """
        url = "https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-de-segmentos-e-setoriais/"
        response = requests.get(url)
        print(f"\n# Conexão à página dos índices de segmentos setoriais\n")
        print(f"Status: {response.status_code} URL: {url}")

        soup = BeautifulSoup(response.text, 'html.parser')
        list_link = []

        for row in soup.find_all('a', href=True):
            if 'saiba mais sobre' in str(row).lower():
                link = row['href'].replace('../../../../', 'https://www.b3.com.br/')
                list_link.append(link)

                print(f"Link encontrado: {link}")

        return list_link
    
    def get_and_save_informacoes_indice(self):
        """
        Extrai informações de cada índice e as salva em arquivos HTML.

        Cada arquivo é nomeado com base na URL do índice correspondente.
        """
        for url in self.get_link():
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                informacoes_indice_html = soup.find_all(id='panel3a') or soup.find_all(id='panel1a')
                html_string = ''.join(str(tag) for tag in informacoes_indice_html)

                # Extrai o nome do arquivo a partir da URL
                name = url.split('/')[-1]
                file_path = join(self.path, f'info_{name}')

                if exists(file_path):
                    print(f'Arquivo já existe: {file_path}. Ignorando a gravação.')
                else:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(html_string)
                        print(f"Informações salvas em: {file_path}")
            
            except requests.exceptions.RequestException as e:
                print(f'Erro de requisição ao acessar {url}: {e}')
            except Exception as e:
                print(f'Erro ao processar {url}: {e}')

if __name__ == '__main__':

    try:
        # Extrai a composição da carteira dos índices setoriais
        carteira_extractor = Extract(config.path_extracted_data, config.INDICES.keys())
        carteira_extractor.get_and_save_informacoes_indice()

    except Exception as e:
        print(f"Ocorreu um erro durante a execução: {e}")
