![Texto alternativo](https://logodownload.org/wp-content/uploads/2019/08/b3-logo-5.png)

# B3 SCRAPING PROJECT

## Descrição
Este projeto tem como objetivo extrair dados da B3 (Bolsa de Valores do Brasil) por meio de web scraping. Utilizando técnicas de scraping, a API permite coletar informações sobre índices de mercado, ações, e outros dados relevantes diretamente do site da B3.

## Funcionalidades

- **Extração de Dados**: Coleta informações atualizadas sobre ações e índices da B3.
- **Tratamento de Dados**: Processa os dados extraídos, limpando e formatando para facilitar a análise.
- **Armazenamento**: Salva os dados em formatos como CSV e TXT para posterior análise.

## Como Usar

### Acesso aos dados
Copie e cole as funções do arquivo para ter acesso aos dados extraidos **[/github_api_acess.py](https://github.com/rianlucascs/b3-scraping-project/blob/master/github_api_acess.py)** no seu projeto.

### Instalação

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
- **Descrição**: Coleta informações sobre diferentes índices do mercado.
- **Funcionalidades**:
  - **Códigos da Carteira**: Lista de códigos das ações que compõem o índice.
  - **Texto de Apresentação**: Breve descrição sobre o índice, incluindo sua finalidade e características.
  - **Arquivo CSV**: Contém dados detalhados sobre o índice, como código, ação, qtde.teórica.

### 2. Horário de Negociação
- **Descrição**: Tabela com os horários de negociação das ações na B3.
- **Funcionalidades**:
  - **Arquivo CSV**: Inclui horários de abertura e fechamento do mercado, diferenciando entre tipos de mercado (à vista, opções, etc.).

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

r