


from os import listdir
from os.path import join, exists
from pandas import DataFrame
import config

class Transform:
    """
    Classe responsável por transformar dados extraídos em um formato processável.

    Esta classe lê arquivos de informações de páginas extraídas, compila os dados
    em um DataFrame do Pandas e exporta o resultado para um arquivo CSV.

    Atributos:
        path_extracted_data (str): Caminho para o diretório onde os dados extraídos estão armazenados.
        path_processed_data (str): Caminho para o diretório onde os dados processados serão salvos.
        dir_page (str): Caminho para o diretório das páginas extraídas.
    """

    def __init__(self, path_extracted_data: str, path_processed_data: str):
        """
        Inicializa a classe Transform.

        :param path_extracted_data: Caminho para o diretório onde os dados extraídos estão armazenados.
        :param path_processed_data: Caminho para o diretório onde os dados processados serão salvos.
        """
        self.path_extracted_data = path_extracted_data
        self.path_processed_data = path_processed_data
        self.dir_page = join(self.path_extracted_data, 'paginas')

    def read_data(self) -> DataFrame:
        """
        Lê os dados dos arquivos de informações e os compila em um DataFrame.

        Esta função percorre todos os diretórios de páginas e lê os arquivos de
        informações correspondentes, retornando um DataFrame com as colunas adequadas.

        :return: Um DataFrame contendo os dados coletados, com colunas para cada atributo relevante.
        """   
        lista = []
        for n_page in listdir(self.dir_page):
            path_n_page = join(self.dir_page, n_page)
            for codigo in listdir(path_n_page):
                if not '.' in codigo:
                    path_infos_codigo = join(path_n_page, codigo, f'infos_{codigo}.txt') 
                    if exists(path_infos_codigo):
                        with open(path_infos_codigo, 'r', encoding='utf-8') as file:
                            data = eval(file.read())
                            lista.append(data)

        headers = ['numero_da_pagina', 'codigo', 'nome_do_pregao', 'codigo_de_negociacao', 'cnpj', 'atividade_principal', 
                   'classificacao_setorial', 'escriturador']
        
        return DataFrame(lista, columns=headers)
    
    def run(self) -> None:
        """
        Executa o processo de leitura e transformação dos dados.

        Esta função chama o método read_data para obter os dados e os salva em um arquivo CSV.
        """
        data = self.read_data()
        data.to_csv(join(self.path_processed_data, 'teste.csv'), sep=';')
        

if __name__ == '__main__':
    transform = Transform(config.path_extracted_data, config.path_processed_data)
    transform.run()
