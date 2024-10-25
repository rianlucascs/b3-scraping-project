from os.path import join, dirname, abspath, exists

path_extracted_data = join(dirname(dirname(dirname(abspath(__file__)))), 'extracted_data', '2. Horário de negociação', 
                               'table.htm')

path_processed_data = join(dirname(dirname(dirname(abspath(__file__)))), 'processed_data', '2. Horário de negociação', 
                               'Tabela_horarios_de_negociacao_no_mercado_de_acoes.xlsx')
    