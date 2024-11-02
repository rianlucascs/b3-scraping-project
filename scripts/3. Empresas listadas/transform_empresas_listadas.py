


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
    """
    
    def __init__(self, path_extracted_data: str, path_processed_data: str):
        """
        Inicializa a classe Transform.

        :param path_extracted_data: Caminho para o diretório onde os dados extraídos estão armazenados.
        :param path_processed_data: Caminho para o diretório onde os dados processados serão salvos.
        """
        self.path_extracted_data = path_extracted_data
        self.path_processed_data = path_processed_data

    def read_data(self) -> DataFrame:
        """
        Lê e compila dados de arquivos de informações em um DataFrame.

        Esta função percorre todos os diretórios dentro do caminho especificado para
        dados extraídos, procurando arquivos nomeados 'infos_<codigo>.txt'. Cada arquivo
        é lido e os dados, que devem estar em formato de lista, são armazenados em uma 
        lista. Essa lista é então convertida em um DataFrame do Pandas.

        Espera-se que cada arquivo contenha uma lista com os seguintes elementos:
        
        - [0]: 'codigo' (Identificador único do item)
        - [1]: 'nome_do_pregao' (Nome do pregão correspondente)
        - [2]: 'codigo_de_negociacao' (Código usado para negociação)
        - [3]: 'cnpj' (Cadastro Nacional da Pessoa Jurídica)
        - [4]: 'atividade_principal' (Descrição da atividade principal)
        - [5]: 'classificacao_setorial' (Classificação do setor econômico)
        - [6]: 'escriturador' (Nome do escriturador responsável)

        A função trata erros ao tentar ler arquivos, imprimindo uma mensagem no console 
        caso ocorra algum problema, mas a execução continuará para os demais arquivos.

        :return: Um DataFrame contendo os dados coletados, com colunas correspondentes
                aos atributos relevantes.
        """
        lista = []
        erros = []
        for codigo in listdir(self.path_extracted_data):
            path_infos_codigo = join(self.path_extracted_data, codigo, f'infos_{codigo}.txt') 
            if exists(path_infos_codigo):
                try:
                    with open(path_infos_codigo, 'r', encoding='utf-8') as file:
                        data = eval(file.read())
                        lista.append(data)
                except OSError as e:
                    erros.append(codigo)
                    print(f"Erro ao ler o arquivo {path_infos_codigo}: {e}")
        if erros:
            print(f'Erros ao ler os arquivos: {erros}')

        headers = ['codigo', 'nome_do_pregao', 'codigo_de_negociacao', 'cnpj', 'atividade_principal', 
                   'classificacao_setorial', 'escriturador']
        
        return DataFrame(lista, columns=headers)
    
    def run(self) -> None:
        """
        Executa o processo de leitura e transformação dos dados.

        Esta função chama o método read_data para obter os dados e os salva em um arquivo CSV.
        """
        data = self.read_data()
        data.to_csv(join(self.path_processed_data, 'todas_empresas_listadas.csv'), sep=';', index=False)
        
if __name__ == '__main__':
    transform = Transform(config.path_extracted_data, config.path_processed_data)
    transform.run()
