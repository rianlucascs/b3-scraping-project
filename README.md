![Texto alternativo](https://logodownload.org/wp-content/uploads/2019/08/b3-logo-5.png)

# B3 SCRAPING PROJECT

## Descrição
Este projeto tem como objetivo extrair dados da B3 ([Bolsa de Valores do Brasil](https://www.b3.com.br/pt_br/para-voce)) por meio de web scraping. 

## Funcionalidades

- **Extração de Dados**: Coleta informações atualizadas sobre ações e índices da B3.

- **Tratamento de Dados**: Processa os dados extraídos, limpando e formatando para facilitar a análise.

- **Armazenamento**: Salva os dados em formatos como CSV e TXT para posterior análise.

- **Disponibilidade**: Disponibiliza os dados para serem acessados em formato de API.

## Como Usar

### Acesso aos dados
Copie e cole as funções do arquivo **[/github_api_acess.ipynb](https://github.com/rianlucascs/b3-scraping-project/blob/master/github_api_acess.ipynb)** em seu projeto para acessar os dados extraídos.

### Instalação do Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/rianlucascs/b3-scraping-project.git

2. Navegue até o diretório do projeto:
    ```bash
    cd b3-scraping-project

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt

4. Execute os scripts:
    ```bash
    extract_composicao_da_carteira_indices_setoriais.py
    extract_informacoes_dos_indices.py
    transform_data_composicao_da_carteira_indices_setoriais.py
    extract_horario_de_negociacao.py
    transform_horario_de_negociacao.py

## Dados Disponíveis

### 1. Índices de Segmentos e Setoriais
- **Descrição**: Coleta informações sobre diferentes índices do mercado [Saiba mais](https://github.com/rianlucascs/b3-scraping-project/blob/master/scripts/1.%20%C3%8Dndices%20de%20Segmentos%20e%20Setoriais/README.md).

- **Dados extraidos**:
  - **Códigos da Carteira**: Lista de códigos das ações que compõem o índice.

  - **Texto de Apresentação**: Breve descrição sobre o índice, incluindo sua finalidade e características.

  - **Arquivo CSV**: Contém: Código do ativo, Ação, Tipo, Quantidade teorica, Participação (%)

### 2. Horário de Negociação
- **Descrição**: Extrai a tabela com os horários de negociação das ações na B3 [Saiba mais](https://github.com/rianlucascs/b3-scraping-project/blob/master/scripts/2.%20Hor%C3%A1rio%20de%20negocia%C3%A7%C3%A3o/README.md).

- **Dados extraidos**:

  - **Arquivo CSV**: Inclui horários de abertura e fechamento do mercado, diferenciando entre tipos de mercado (à vista, opções, etc.).

### 3. Empresas Listadas (Renda variável)

- **Descrição**: Extrai informações sobre todas as ações listadas na B3 [Saiba mais](https://github.com/rianlucascs/b3-scraping-project/blob/master/scripts/3.%20Empresas%20listadas/README.md).

- **Dados extraidos**:

  - **Arquivo CSV**: Inclui: Código do ativo, Nome do pregão, Código de negociação, CNPJ, Atividade principal, Classificação setorial, Escriturador
  
  codigo;nome_do_pregao;codigo_de_negociacao;cnpj;atividade_principal;classificacao_setorial;escriturador


## Exemplos de Uso

- Para obter os códigos de ações de um índice específico, como o IDIV (Índice de Dividendos):
  
  ```bash
  # Obtém os códigos de ações do índice IDIV
  codigos = get_codigos('IDIV')
  
  # Exibe os códigos obtidos
  print("Códigos de ações do IDIV:")
  print(codigos)

- Para obter a tabela com os horarios de negociação da bolsa

  ```bash
  # Obtém a tabela com os horários de negociação
  horarios = get_tabela_horario()

  # Exibe os horários de negociação
  print("Tabela de horários de negociação do mercado à vista:")
  print(horarios)

## Contato

Estou à disposição para esclarecer dúvidas ou fornecer mais informações. Você pode entrar em contato através das seguintes opções:

- **LinkedIn:** [Visite meu perfil no LinkedIn](www.linkedin.com/in/rian-lucas)
- **GitHub:** [Explore meu repositório no GitHub](https://github.com/rianlucascs)
- **Celular:** +55 61 96437-9500


Fico sempre aberto a colaborações e oportunidades de networking!
