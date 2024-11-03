import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import config
from typing import List

class ExtractAndTransform:
    """
    Classe para extrair, transformar e salvar dados de uma tabela HTML.

    Esta classe realiza a extração de dados de uma tabela localizada em uma 
    URL específica, transforma esses dados em um DataFrame do pandas e, 
    em seguida, salva o DataFrame em um arquivo CSV.

    Attributes:
        path_processed_data (str): Caminho para o arquivo CSV onde os dados 
            processados serão salvos.
        url (str): URL da página web de onde os dados serão extraídos.
        headers (list): Lista de cabeçalhos a serem utilizados no DataFrame 
            resultante.

    Methods:
        ``extract() -> List[str]``:
            Extrai os dados da tabela HTML localizada na URL especificada.

        ``transform(extract_data: List[str]) -> DataFrame``:
            Transforma os dados extraídos em um DataFrame do pandas.

        ``save(df_data: DataFrame) -> None``:
            Salva o DataFrame em um arquivo CSV.

        ``run()``:
            Executa o processo de extração, transformação e salvamento.
    """
    
    def __init__(self, path_processed_data: str, url: str, headers: List[str]):
        """
        Inicializa a instância da classe ExtractAndTransform.

        Args:
            path_processed_data (str): Caminho para o arquivo CSV onde os dados processados serão salvos.
            url (str): URL da página web de onde os dados serão extraídos.
            headers (list): Lista de cabeçalhos a serem utilizados no DataFrame resultante.
        """
        self.path_processed_data = path_processed_data
        self.url = url
        self.headers = headers
    
    def extract(self) -> List[str]:
        """
        Extrai os dados da tabela HTML localizada na URL especificada.

        Realiza uma requisição GET à URL e utiliza BeautifulSoup para analisar o conteúdo HTML.
        Retorna uma lista de listas, onde cada sublista representa uma linha da tabela.

        Returns:
            list: Lista contendo as linhas da tabela extraídas. Retorna uma lista vazia se ocorrer um erro.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, 'html.parser')
            tabela = soup.find('table')
            if tabela is None:
                print("Tabela não encontrada na página.")
                return []
            dados = []
            for tr in tabela.find_all('tr')[1:]:
                linha = [td.get_text(strip=True) for td in tr.find_all('td')]
                if linha:
                    dados.append(linha)
            print(f"Dados extraídos: {len(dados)} linhas.")
            return dados
        except requests.RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")
            return []
        except Exception as e:
            print(f"Ocorreu um erro durante a extração: {e}")
            return []

    def transform(self, extract_data: List[str]) -> DataFrame:
        """
        Transforma os dados extraídos em um DataFrame do pandas.

        Args:
            extract_data (list): Lista de listas com os dados extraídos.

        Returns:
            DataFrame: DataFrame contendo os dados transformados. Retorna um DataFrame vazio se não houver dados.
        """
        if not extract_data:
            print("Nenhum dado para transformar.")
            return DataFrame()
        
        df_data = DataFrame(extract_data, columns=self.headers)
        print("Dados transformados em DataFrame.")
        return df_data
    
    def save(self, df_data: DataFrame) -> None:
        """
        Salva o DataFrame em um arquivo CSV.

        Args:
            df_data (DataFrame): DataFrame que contém os dados a serem salvos.

        Returns:
            None
        """
        try:
            df_data.to_csv(self.path_processed_data, index=False, encoding='utf-8')
            print(f"Dados salvos em: {self.path_processed_data}")
        except Exception as e:
            print(f"Erro ao salvar os dados: {e}")

    def run(self):
        """Executa o processo de extração, transformação e salvamento."""
        extract_data = self.extract()
        transform_data = self.transform(extract_data)
        self.save(transform_data)

if __name__ == '__main__':
    extract_and_transform = ExtractAndTransform(
        config.path_processed_data, 
        config.url,
        config.headers
        )
    extract_and_transform.run()
    