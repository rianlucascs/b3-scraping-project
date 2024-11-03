
import config
from os.path import join, exists
from os import listdir, makedirs
from pandas import read_csv, DataFrame

import difflib
from bs4 import BeautifulSoup
import textwrap
from typing import List

__python__ = 3.10

class Transform:
    """
    Classe para transformação e processamento de dados extraídos.

    Esta classe é responsável por localizar, ler, processar e salvar dados 
    em formatos CSV e HTML. Ela lida com a criação de diretórios, leitura de 
    arquivos, renomeação de colunas e salvamento de arquivos processados, 
    permitindo uma organização eficiente dos dados de acordo com índices 
    fornecidos.

    Attributes:
        path_extracted_data (str): Caminho para o diretório onde os dados 
            extraídos estão armazenados.
        path_processed_data (str): Caminho para o diretório onde os dados 
            processados serão salvos.
        indices (list): Lista de índices a serem processados.
        dict_indices (dict): Dicionário que mapeia os índices a suas descrições.

    Methods:
        ``loc_data_csv(indice: str) -> str``:
            Encontra o arquivo CSV correspondente a um índice.
        
        ``loc_data_htm(indice: str) -> str``:
            Localiza um arquivo HTML correspondente a um índice.
        
        ``read_data_csv(file: str, skiprows: int = 1, 
                         skipfooter: int = 2, na_values: List[str] = ['NaN', '']) -> DataFrame``:
            Lê um arquivo CSV e processa seus dados.

        ``read_data_htm(file: str, encoding: str = 'utf-8') -> str``:
            Lê um arquivo HTML e extrai o texto.

        ``save_codigos_carteira_setor(path: str, file_name: str, 
                                       file_csv: DataFrame, update: bool = False) -> None``:
            Salva os códigos de ações extraídos em um arquivo de texto.

        ``save_informacoes_sobre_o_setor(path: str, file_name: str, 
                                           file_htm: str, update: bool = False) -> None``:
            Salva informações formatadas sobre um setor em um arquivo de texto.

        ``save_csv_2(path: str, file_csv: DataFrame, indice: str, update: bool = False) -> None``:
            Salva um DataFrame como um arquivo CSV.

        ``create_directory(indice: str) -> str``:
            Cria um diretório para o índice, se não existir.

        ``process_csv(indice: str, new_dir: str, update: bool = False) -> DataFrame``:
            Processa e salva os dados de um arquivo CSV para um índice.

        ``process_html(indice: str, new_dir: str, update: bool = False) -> None``:
            Processa e salva os dados de um arquivo HTML para um índice.

        ``execution(update: bool = True) -> None``:
            Executa o fluxo principal de transformação de dados.
    """
    
    def __init__(self, path_extracted_data: str, path_processed_data: str, indices: str, dict_indices):
        """
        Inicializa a classe Transform com os caminhos de dados e índices.

        Args:
            path_extracted_data (str): Caminho para o diretório onde os dados extraídos estão armazenados.
            path_processed_data (str): Caminho para o diretório onde os dados processados serão salvos.
            indices (list): Lista de índices a serem processados.
            dict_indices (dict): Dicionário que mapeia os índices a suas descrições.
        """
        self.path_extracted_data = path_extracted_data
        self.path_processed_data = path_processed_data
        self.indices = indices
        self.dict_indices = dict_indices

    def loc_data_csv(self, indice: str) -> str:
        """
        Encontra o arquivo CSV correspondente a um índice no diretório de dados.

        Args:
            indice (str): O índice a ser buscado.

        Returns:
            str: Nome do arquivo CSV encontrado, ou None se não houver.
        """
        for file in listdir(self.path_extracted_data):
            if indice.lower() in file.lower() and file.split('.')[-1] == 'csv':
                return file
    
    def loc_data_htm(self, indice: str) -> str:
        """
        Localiza um arquivo HTML correspondente a um índice.

        A função procura primeiro por um arquivo cujo nome contém o índice
        (ignorando maiúsculas/minúsculas). Se não encontrado, ela calcula
        a similaridade entre os nomes dos arquivos HTML e o nome do índice
        fornecido, retornando o arquivo com a maior similaridade.

        Args:
            indice (str): O índice a ser buscado no nome do arquivo.

        Returns:
            str: O nome do arquivo HTML correspondente ou o mais similar.
        """
        files = [file for file in listdir(self.path_extracted_data) if file.endswith('.htm')]

        if not files:
            raise FileNotFoundError('Nenhum arquivo HTML encontrado.')
        
        # Tenta encontrar um arquivo exato
        for file in files:
            if f'-{indice.lower()}-' in file.lower():
                return file

        # Se não encontrado, calcula a similaridade
        result = {file: difflib.SequenceMatcher(None, file.lower(), self.dict_indices[indice].lower()).ratio() for file in files}

        return max(result, key=result.get)

    def read_data_csv(self, file: str, skiprows: int = 1, skipfooter: int = 2, na_values : List[str] = ['NaN', '']) -> DataFrame:
        """
        Lê um arquivo CSV e processa seus dados.

        Esta função realiza a leitura de um arquivo CSV localizado no diretório
        especificado, aplicando configurações específicas para formatação e tratamento
        de dados, como remoção de linhas desnecessárias e renomeação de colunas.

        Args:
            file (str): O nome do arquivo CSV a ser lido.
            skiprows (int, optional): Número de linhas a serem ignoradas no início do arquivo. Padrão é 1.
            skipfooter (int, optional): Número de linhas a serem ignoradas no final do arquivo. Padrão é 2.
            na_values (list, optional): Valores a serem considerados como NaN. Padrão é ['NaN', ''].

        Returns:
            DataFrame: Um DataFrame do Pandas contendo os dados processados, com
            colunas renomeadas e a última coluna removida.

        Raises:
            FileNotFoundError: Se o arquivo não for encontrado.
            Exception: Para outros erros durante a leitura do arquivo.
        """
        if na_values is None:
            na_values = ['NaN', '']
        try:
            file_csv = read_csv(
                join(self.path_extracted_data, file), 
                encoding='ISO-8859-1', 
                delimiter=';', 
                skiprows=skiprows, 
                skipfooter=skipfooter, 
                na_values=na_values, 
                on_bad_lines='warn', 
                engine='python'
            ).reset_index()
            file_csv.columns = ['Código', 'Ação', 'Tipo', 'Qtde. Teórica', 'Part. (%)', '']
            file_csv = file_csv.iloc[:, :-1]  # Remove a última coluna
            return file_csv
        except FileNotFoundError:
            print(f"Erro: O arquivo '{file}' não foi encontrado.")
            raise
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            raise

    def read_data_htm(self, file: str, encoding: str = 'utf-8') -> str:
        """
        Lê um arquivo HTML e extrai o texto.

        Esta função abre um arquivo HTML, analisa seu conteúdo com BeautifulSoup
        e retorna o texto extraído. O texto é retornado como uma string única, 
        com espaços extras removidos.

        Args:
            file (str): O nome do arquivo HTML a ser lido.
            encoding (str): O encoding do arquivo (padrão é 'utf-8').

        Returns:
            str: O texto extraído do arquivo HTML.

        Raises:
            FileNotFoundError: Se o arquivo não for encontrado.
            Exception: Se houver um erro ao ler o arquivo.
        """
        file_path = join(self.path_extracted_data, file)
        
        if not exists(file_path):
            raise FileNotFoundError(f'O arquivo {file_path} não foi encontrado.')

        try:
            with open(file_path, 'r', encoding=encoding) as htm:
                soup = BeautifulSoup(htm, 'html.parser')
                return soup.get_text(strip=True)
        except Exception as e:
            raise Exception(f'Erro ao ler o arquivo {file_path}: {e}')

    def save_codigos_carteira_setor(self, path: str, file_name: str, file_csv: str, update: bool = False) -> None:
        """
        Salva os códigos de ações extraídos em um arquivo de texto.

        O arquivo é criado no diretório especificado, e a atualização é feita se
        o arquivo já existir e o parâmetro update for True.

        Args:
            path (str): Diretório onde o arquivo será salvo.
            file_name (str): Nome base do arquivo.
            file_csv (DataFrame): DataFrame contendo os códigos a serem salvos.
            update (bool): Se True, força a atualização do arquivo existente.
        """
        new_file = join(path, f'Códigos_{file_name}.txt')
        if not exists(new_file) or update is True:
            try:
                with open(new_file, 'w', encoding='utf-8') as file:
                    
                    file.write('\n'.join(file_csv['Código'].values) + '\n') # <---!!
                
                print(f'Códigos salvos em {new_file}.') 
            except Exception as e:
                print(f'Erro ao salvar o arquivo {e}.')
        else:
            print(f'O arquivo já existe: {new_file}')

    def save_informacoes_sobre_o_setor(self, path: str, file_name: str, file_htm: str, update=False) -> None:
        """
        Salva informações formatadas sobre um setor em um arquivo de texto.

        O conteúdo é escrito em um formato legível, com quebras de linha, e o arquivo
        é criado se não existir ou se a atualização for solicitada.

        Args:
            path (str): Diretório onde o arquivo será salvo.
            file_name (str): Nome base do arquivo (sem extensão).
            file_htm (str): Conteúdo HTML a ser escrito no arquivo.
            update (bool): Se True, força a atualização do arquivo existente.

        Returns:
            None
        """
        new_file = join(path, f'Apresentação_{file_name}.txt')

        if not exists(new_file) or update:
            try:
                with open(new_file, 'w', encoding='utf-8') as file:
                    file.write(textwrap.fill(file_htm, width=50))
                print(f'Apresentação salva em {new_file}.')
            except OSError as e:
                print(f'Erro ao salvar o arquivo: {e}')
        else:
            print(f'O arquivo já existe: {new_file}')
        
    def save_csv_2(self, path: str, file_csv: DataFrame, indice: str, update: bool = False) -> None:
        """
        Salva um DataFrame como um arquivo CSV.

        O arquivo é salvo no diretório especificado e nomeado como 'Tabela_{indice}.csv'.
        A atualização é feita se o arquivo já existir e o parâmetro update for True.

        Args:
            path (str): Diretório onde o arquivo será salvo.
            file_csv (DataFrame): DataFrame contendo os dados a serem salvos.
            indice (str): Índice para nomear o arquivo CSV.
            update (bool): Se True, força a atualização do arquivo existente.

        Returns:
            None
        """
        try:
            file_path = join(path, f'Tabela_{indice}.csv')
            if not exists(file_path) or update:
                file_csv.to_csv(file_path, index=False, encoding='utf-8')
                print(f'Arquivo salvo em: {file_path}')
            else:
                print(f'O arquivo já existe: {file_path}')
        except Exception as e:
            print(f'Erro ao salvar o arquivo: {e}')
    
    def create_directory(self, indice: str) -> str:
        """
        Cria um diretório para o índice, se não existir.
        
        Args:
            indice (str): O índice para o qual o diretório será criado.
        
        Returns:
            str: O caminho do diretório criado.
        """
        new_dir = join(self.path_processed_data, 'Setores', indice)
        if not exists(new_dir):
            makedirs(new_dir)
            print(f'Diretório criado: {new_dir}')
        return new_dir

    def process_csv(self, indice: str, new_dir: str, update: bool = False) -> DataFrame:
        """
        Processa e salva os dados de um arquivo CSV para um índice.

        Essa função coordena a localização, leitura e salvamento do arquivo CSV.

        Args:
            indice (str): O índice do qual os dados serão processados.
            new_dir (str): Diretório onde os arquivos processados serão salvos.
            update (bool): Se True, força a atualização dos arquivos existentes.

        Returns:
            DataFrame: DataFrame com os dados do índice processado.
        """
        file_name = self.loc_data_csv(indice)
        file_csv = self.read_data_csv(file_name)
        self.save_codigos_carteira_setor(new_dir, indice, file_csv, update=update)
        self.save_csv_2(new_dir, file_csv, indice, update=update)
        return file_csv

    def process_html(self, indice: str, new_dir: str, update: bool = False) -> None:
        """
        Processa e salva os dados de um arquivo HTML para um índice.

        Essa função coordena a localização, leitura e salvamento do conteúdo HTML.

        Args:
            indice (str): O índice do qual os dados serão processados.
            new_dir (str): Diretório onde os arquivos processados serão salvos.
            update (bool): Se True, força a atualização dos arquivos existentes.
        """
        file_name = self.loc_data_htm(indice)
        file_htm = self.read_data_htm(file_name)
        self.save_informacoes_sobre_o_setor(new_dir, indice, file_htm, update=update)

    def execution(self, update: bool = True) -> None:
        """
        Executa o fluxo principal de transformação de dados.

        Esta função itera sobre todos os índices e processa os dados correspondentes, 
        lidando com exceções durante o processo.

        Args:
            update (bool): Se True, força a atualização dos arquivos existentes.
        """
        for indice in self.indices:
            try:
                new_dir = self.create_directory(indice)
                file_csv = self.process_csv(indice, new_dir, update)
                self.process_html(indice, new_dir, update)

            except Exception as e:
                print(f'Erro ao processar o índice {indice}: {e}')

if __name__ == '__main__':
    transform_composicao_da_carteira = Transform(
        config.path_extracted_data, 
        config.path_processed_data, 
        config.INDICES.keys(),
        config.INDICES)
    
    transform_composicao_da_carteira.execution(
        update=True
        )
    


