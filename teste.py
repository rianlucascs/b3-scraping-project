import requests

def get_codigos(setor:str='IDIV', sa:bool=True) -> list:
    """
    Obtém a lista de códigos de ações de um setor específico a partir de um arquivo TXT no GitHub.
    """
    url = f'https://raw.githubusercontent.com/rianlucascs/b3-scraping-project/master/processed_data/1.%20%C3%8Dndices%20de%20Segmentos%20e%20Setoriais/Setores/{setor}/C%C3%B3digos_{setor}.txt'  
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f'Erro ao acessar a página: {response.status_code}, setor: {setor}')
    lista = [item.strip() for item in response.text.splitlines() if item.strip()]
    if sa:
        lista = [f'{item}.SA' for item in lista]
    return lista
