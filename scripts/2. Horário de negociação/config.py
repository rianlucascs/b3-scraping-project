from os.path import join, dirname, abspath

# Define o diretório base para os caminhos dos dados
diretorio_base = dirname(dirname(dirname(abspath(__file__))))

# Especifica os caminhos para os dados extraídos e processados
path_extracted_data = join(diretorio_base, 'extracted_data', '2. Horário de negociação', 'table.htm')
path_processed_data = join(diretorio_base, 'processed_data', '2. Horário de negociação', 'Tabela_horarios_de_negociacao_no_mercado_de_acoes.csv')

# URL para a extração de dados
url = 'https://www.b3.com.br/pt_br/solucoes/plataformas/puma-trading-system/para-participantes-e-traders/horario-de-negociacao/acoes/'

# Define os cabeçalhos das colunas para o DataFrame
headers = ['Mercado1', 
           'Cancelamento de Ofertas', 'Cancelamento de Ofertas',
           'Pré-Abertura', 'Pré-Abertura',
           'Negociação', 'Negociação',
           'Call de Fechamento', 'Call de Fechamento',
           'After-Market3 - Cancelamento de Ofertas4', 'After-Market3 - Cancelamento de Ofertas4',
           'After-Market3 - Negociação', 'After-Market3 - Negociação',
           'Cancelamento de Ofertas4', 'Cancelamento de Ofertas4'
           ]