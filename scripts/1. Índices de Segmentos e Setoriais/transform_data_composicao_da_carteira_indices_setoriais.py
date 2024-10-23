
import config
from os.path import join, exists
from os import listdir, makedirs
from pandas import read_csv

import difflib
from bs4 import BeautifulSoup

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
            if indice.lower() in file.lower():
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
        try:
            file_csv = read_csv(join(self.path_extracted_data, file), encoding='ISO-8859-1', delimiter=';', 
                                skiprows=skiprows, skipfooter=skipfooter, na_values=na_values, 
                                on_bad_lines='warn', engine='python').reset_index()
            file_csv.columns = ['Código', 'Ação', 'Tipo', 'Qtde. Teórica', 'Part. (%)', '']
            file_csv = file_csv.iloc[:, :-1]  # Remove a última coluna

            return file_csv
        except FileNotFoundError:
            print(f"Erro: O arquivo '{file}' não foi encontrado.")
            raise
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            raise

    def read_data_htm(self, file):
        with open(join(self.path_extracted_data, file), 'a', encoding='utf-8') as f:
            f.
    
    def save_codigo(self, path, file_name, file_csv):
        """
        Salva os códigos de ações em um arquivo de texto.

        Args:
            path (str): O diretório onde o arquivo será salvo.
            file_name (str): O nome base do arquivo.
            file_csv (DataFrame): O DataFrame que contém os códigos.
        """
        new_file = join(path, f'Códigos_{file_name}.txt')
        if not exists(new_file):
            try:
                with open(new_file, 'w', encoding='utf-8') as file:
                    file.write(file_csv['Código'].to_string(index=False, header=False))
                print(f'Códigos salvos em {new_file}.')
            except Exception as e:
                print(f'Erro ao salvar o arquivo {e}.')
        else:
            print(f'O arquivo já existe: {new_file}')

    def save_informacoes_sobre_o_setor(self, path, file):
        pass

    def execution(self):

        for indice in self.indices:

            new_dir = join(self.path_processed_data, 'Setores', indice)
            if not exists(new_dir):
                makedirs(new_dir)
            
            file_name = self.loc_data_csv(indice)
            file_csv = self.read_data_csv(file_name)
            self.save_codigo(new_dir, indice, file_csv)

            file_name = self.loc_data_htm(indice)
            file_htm =

            
            

if __name__ == '__main__':
    transform_composicao_da_carteira = Transform(config.path_extracted_data, config.path_processed_data, config.INDICES.keys(),
                                                 config.INDICES)
    
    for i in config.INDICES.keys():
        print(i, transform_composicao_da_carteira.loc_data_html(i))
    


