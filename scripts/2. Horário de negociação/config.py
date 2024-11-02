from os.path import join, dirname, abspath

path_extracted_data = join(dirname(dirname(dirname(abspath(__file__)))), 'extracted_data', '2. Horário de negociação', 
                               'table.htm')

path_processed_data = join(dirname(dirname(dirname(abspath(__file__)))), 'processed_data', '2. Horário de negociação', 
                               'Tabela_horarios_de_negociacao_no_mercado_de_acoes.csv')

url = 'https://www.b3.com.br/pt_br/solucoes/plataformas/puma-trading-system/para-participantes-e-traders/horario-de-negociacao/acoes/'

headers = ['Mercado1', 
           'Cancelamento de Ofertas', 'Cancelamento de Ofertas',
           'Pré-Abertura', 'Pré-Abertura',
           'Negociação', 'Negociação',
           'Call de Fechamento', 'Call de Fechamento',
           'After-Market3 - Cancelamento de Ofertas4', 'After-Market3 - Cancelamento de Ofertas4',
           'After-Market3 - Negociação', 'After-Market3 - Negociação',
           'Cancelamento de Ofertas4', 'Cancelamento de Ofertas4'
           ]