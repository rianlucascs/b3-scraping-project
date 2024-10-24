
import config
from os.path import join, exists
from os import listdir, makedirs
from pandas import read_csv

import difflib
from bs4 import BeautifulSoup
import textwrap
import shutil

class Transform:
    
    def __init__(self, path_extracted_data, path_processed_data, indices, dict_indices):
        self.path_extracted_data = path_extracted_data
        self.path_processed_data = path_processed_data
        self.indices = indices
        self.dict_indices = dict_indices

    def loc_data_csv(self, indice):
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
    
    def loc_data_htm(self, indice):
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

    def read_data_csv(self, file, skiprows=1, skipfooter=2, na_values=['NaN', '']):
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

    def read_data_htm(self, file, encoding='utf-8'):
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

    def save_codigos_carteira_setor(self, path, file_name, file_csv, update=False):
        """
        Salva os códigos de ações em um arquivo de texto.

        Args:
            path (str): O diretório onde o arquivo será salvo.
            file_name (str): O nome base do arquivo.
            file_csv (DataFrame): O DataFrame que contém os códigos.
        """
        new_file = join(path, f'Códigos_{file_name}.txt')
        if not exists(new_file) or update is True:
            try:
                with open(new_file, 'w', encoding='utf-8') as file:
                    file.write(file_csv['Código'].to_string(index=False, header=False))
                print(f'Códigos salvos em {new_file}.')
            except Exception as e:
                print(f'Erro ao salvar o arquivo {e}.')
        else:
            print(f'O arquivo já existe: {new_file}')

    def save_informacoes_sobre_o_setor(self, path, file_name, file_htm, update=False):
        """
        Salva informações sobre um setor em um arquivo de texto.

        Esta função cria um arquivo de texto com uma apresentação do setor,
        formatando o conteúdo com quebras de linha. O arquivo é criado se não
        existir ou se a atualização for solicitada.

        Args:
            path (str): O diretório onde o arquivo será salvo.
            file_name (str): O nome base do arquivo (sem extensão).
            file_htm (str): O conteúdo HTML a ser escrito no arquivo.
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
            except IOError as e:
                print(f'Erro ao salvar o arquivo: {e}')
        else:
            print(f'O arquivo já existe: {new_file}')
    
    ### XXX ##
    def save_csv(self, path, file_name, indice):
        """
        Copia um arquivo CSV de um diretório de origem para um diretório de destino
        e altera seu nome.

        Args:
            path (str): O diretório de destino onde o arquivo será salvo. Deve existir.
            file_name (str): O nome do arquivo CSV que será copiado do diretório de origem.
            indice (str): O índice usado para renomear o arquivo copiado. O novo nome do arquivo será
                        formatado como 'Tabela_{indice}.csv'.

        Returns:
            None: Esta função não retorna nenhum valor. O arquivo é salvo no diretório especificado.

        Raises:
            FileNotFoundError: Se o arquivo de origem não for encontrado.
            OSError: Se o diretório de destino não existir ou se ocorrer um erro na cópia do arquivo.
        """
        if not exists(path):
            raise OSError(f'O diretório de destino não existe: {path}')
        
        src_file = join(self.path_extracted_data, file_name)
        dest_file = join(path, f'Tabela_{indice}.csv')

        try:
            shutil.copy(src_file, dest_file)
            print(f'Arquivo salvo como: {dest_file}')
        except FileNotFoundError:
            raise FileNotFoundError(f'O arquivo de origem não foi encontrado: {src_file}')
        except Exception as e:
            raise OSError(f'Erro ao copiar o arquivo: {e}')
        
    def save_csv_2(self, path, file_csv, indice, update=False):
        """
        Salva um DataFrame como um arquivo CSV.

        Args:
            path (str): O diretório onde o arquivo será salvo.
            file_csv (DataFrame): O DataFrame que contém os dados a serem salvos.
            indice (str): O índice para nomear o arquivo CSV.
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
    
    def create_directory(self, indice):
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

    def process_csv(self, indice, new_dir, update):
        """
        Processa e salva os dados CSV para o índice.
        
        Args:
            indice (str): O índice do qual os dados serão processados.
            new_dir (str): O diretório onde os arquivos serão salvos.
            update (bool): Se True, força a atualização dos arquivos existentes.
        
        Returns:
            DataFrame: O DataFrame com os dados do índice.
        """
        file_name = self.loc_data_csv(indice)
        file_csv = self.read_data_csv(file_name)
        self.save_codigos_carteira_setor(new_dir, indice, file_csv, update=update)
        self.save_csv_2(new_dir, file_csv, indice, update=update)
        return file_csv

    def process_html(self, indice, new_dir, update):
        """
        Processa e salva os dados HTML para o índice.
        
        Args:
            indice (str): O índice do qual os dados serão processados.
            new_dir (str): O diretório onde os arquivos serão salvos.
            update (bool): Se True, força a atualização dos arquivos existentes.
        """
        file_name = self.loc_data_htm(indice)
        file_htm = self.read_data_htm(file_name)
        self.save_informacoes_sobre_o_setor(new_dir, indice, file_htm, update=update)

    def execution(self, update=True):
        """
        Executa o fluxo principal de transformação de dados.
        
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
        update=False
        )
    


