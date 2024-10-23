![Texto alternativo](https://logodownload.org/wp-content/uploads/2019/08/b3-logo-5.png)

# B3 SCRAPING PROJECT

## Descrição
Este projeto tem como objetivo extrair dados da B3 (Bolsa de Valores do Brasil) por meio de web scraping. Utilizando técnicas de scraping, a API permite coletar informações sobre índices de mercado, ações, e outros dados relevantes diretamente do site da B3.

## Funcionalidades

- **Extração de Dados**: Coleta informações atualizadas sobre ações e índices da B3.

- **Tratamento de Dados**: Processa os dados extraídos, limpando e formatando para facilitar a análise.

- **Armazenamento**: Salva os dados em formatos como CSV e TXT para posterior análise.

## Como Usar

Copie e cole as funções do arquivo github_api_acess.py no seu projeto.

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