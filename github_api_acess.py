import requests
from pandas import read_csv
from io import StringIO

# 1. Índices de Segmentos e Setoriais

def get_codigos(setor:str='IDIV') -> list:
    """
    Obtém a lista de códigos de ações de um setor específico a partir de um arquivo TXT no GitHub.

    Esta função faz uma requisição a uma URL que contém os códigos das ações de um determinado setor.
    Se a requisição for bem-sucedida, os códigos são processados e retornados como uma lista.

    Args:
        setor (str): O nome do setor cujos códigos de ações devem ser obtidos. Os setores disponíveis são:
            - 'IDIV': Índice Dividendos BM&FBOVESPA (IDIV B3)
            - 'MLCX': Índice MidLarge Cap (MLCX B3)
            - 'SMLL': Índice Small Cap (SMLL B3)
            - 'IVBX': Índice Valor (IVBX 2 B3)
            - 'AGFS': Índice Agronegócio B3 (IAGRO B3)
            - 'IFNC': Índice BM&FBOVESPA Financeiro (IFNC B3)
            - 'IBEP': Índice Bovespa B3 Empresas Privadas (Ibov B3 Empresas Privadas)
            - 'IBEE': Índice Bovespa B3 Estatais (Ibov B3 Estatais)
            - 'IBHB': Índice Bovespa Smart High Beta B3 (Ibov Smart High Beta B3)
            - 'IBLV': Índice Bovespa Smart Low Volatility B3 (Ibov Smart Low B3)
            - 'IMOB': Índice Imobiliário (IMOB B3)
            - 'UTIL': Índice Utilidade Pública BM&FBOVESPA (UTIL B3)
            - 'ICON': Índice de Consumo (ICON B3)
            - 'IEEX': Índice de Energia Elétrica (IEE B3)
            - 'IFIL': Índice de Fundos de Investimentos Imobiliários de Alta Liquidez (IFIX L B3)
            - 'IMAT': Índice de Materiais Básicos BM&FBOVESPA (IMAT B3)
            - 'INDX': Índice do Setor Industrial (INDX B3)
            - 'IBSD': Índice Bovespa Smart Dividendos B3 (Ibov Smart Dividendos B3)
            - 'BDRX': Índice de BDRs Não Patrocinados-GLOBAL (BDRX B3)
            - 'IFIX': Índice de Fundos de Investimentos Imobiliários (IFIX B3)

    Returns:
        list: Uma lista contendo os códigos das ações do setor. Se a requisição falhar, a função levanta uma exceção.
    """
    url = f'https://raw.githubusercontent.com/rianlucascs/b3-scraping-project/master/processed_data/1.%20%C3%8Dndices%20de%20Segmentos%20e%20Setoriais/Setores/{setor}/C%C3%B3digos_{setor}.txt'  
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise ValueError(f'Erro ao acessar a página: {e}')
    return [item.strip() for item in response.text.splitlines()]

def get_apresentacao(setor:str) -> str: 
    """
    Obtém a apresentação de um setor a partir de um arquivo TXT em um repositório no GitHub.

    Args:
        setor (str): O nome do setor para buscar a apresentação.

    Returns:
        str: O conteúdo da apresentação.

    Raises:
        ValueError: Se não for possível acessar a página.
    """
    url = f'https://raw.githubusercontent.com/rianlucascs/b3-scraping-project/master/processed_data/1.%20%C3%8Dndices%20de%20Segmentos%20e%20Setoriais/Setores/{setor}/Apresenta%C3%A7%C3%A3o_{setor}.txt'
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise ValueError(f'Erro ao acessar a página: {e}')
    return response.text

def get_tabela(setor:str):
    """
    Obtém a tabela de ações de um setor específico a partir de um arquivo CSV no GitHub.

    Esta função faz uma requisição a uma URL que contém a tabela das ações de um determinado setor.
    Se a requisição for bem-sucedida, a tabela é lida e retornada como um DataFrame.

    Args:
        setor (str): O nome do setor cujos dados devem ser obtidos.

    Returns:
        DataFrame: Um DataFrame contendo os dados da tabela. Se a requisição falhar, a função levanta uma exceção.
    """
    url = f'https://raw.githubusercontent.com/rianlucascs/b3-scraping-project/master/processed_data/1.%20%C3%8Dndices%20de%20Segmentos%20e%20Setoriais/Setores/{setor}/Tabela_{setor}.csv'
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise ValueError(f'Erro ao acessar a página: {e}')
    return read_csv(StringIO(response.text), delimiter=',')

# 2. Horário de negociação

if __name__ == '__main__':
    
    setor = 'IDIV'
    # print(get_apresentacao(setor))
    # print(get_codigos(setor))

    print(get_tabela(setor))