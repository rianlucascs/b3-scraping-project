import extract_informacoes_dos_indices

indices = [
        "IDIV", "MLCX", "SMLL", "IVBX", "AGFS", "IFNC", "IBEP", "IBEE",
        "IBHB", "IBLV", "IMOB", "UTIL", "ICON", "IEEX", "IFIL", "IMAT",
        "INDX", "IBSD", "BDRX", "IFIX"
    ]

lista = extract_informacoes_dos_indices.Extract('', indices).get_link()


keys = {
    'IDIV': 'Índice Dividendos BM&FBOVESPA (IDIV B3)',
    'MLCX': 'Índice MidLarge Cap (MLCX B3)',
    'SMLL': 'Índice Small Cap (SMLL B3)',
    'IVBX': 'Índice Valor (IVBX 2 B3)',
    'AGFS': 'Índice Agronegócio B3 (IAGRO B3)',
    'IFNC': 'Índice BM&FBOVESPA Financeiro (IFNC B3)',
    'IBEP': 'Índice Bovespa B3 Empresas Privadas (Ibov B3 Empresas Privadas)',
    'IBEE': 'Índice Bovespa B3 Estatais (Ibov B3 Estatais)',
    'IBHB': 'Índice Bovespa Smart High Beta B3 (Ibov Smart High Beta B3)',
    'IBLV': 'Índice Bovespa Smart Low Volatility B3 (Ibov Smart Low Vol B3)',
    'IMOB': 'Índice Imobiliário (IMOB B3)',
    'UTIL': 'Índice Utilidade Pública BM&FBOVESPA (UTIL B3)',
    'ICON': 'Índice de Consumo (ICON B3)',
    'IEEX': 'Índice de Energia Elétrica (IEE B3)',
    'IFIL': 'Índice de Fundos de Investimentos Imobiliários de Alta Liquidez (IFIX L B3)',
    'IMAT': 'Índice de Materiais Básicos BM&FBOVESPA (IMAT B3)',
    'INDX': 'Índice do Setor Industrial (INDX B3)',
    'IBSD': 'Índice Bovespa Smart Dividendos B3 (Ibov Smart Dividendos B3)',
    'BDRX': 'Índice de BDRs Não Patrocinados-GLOBAL (BDRX B3)',
    'IFIX': 'Índice de Fundos de Investimentos Imobiliários (IFIX B3)'
}