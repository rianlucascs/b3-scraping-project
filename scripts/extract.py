
from os.path import dirname, join, abspath
import extract_composicao_da_carteira_indices_setoriais
import extract_informacoes_dos_indices

if __name__ == '__main__':
    # Define o caminho para o diretório onde os dados brutos serão salvos
    path_data_raw = join(dirname(dirname(abspath(__file__))), 'data_raw')
    
    # Lista de índices a serem processados
    indices = [
        "IDIV", "MLCX", "SMLL", "IVBX", "AGFS", "IFNC", "IBEP", "IBEE",
        "IBHB", "IBLV", "IMOB", "UTIL", "ICON", "IEEX", "IFIL", "IMAT",
        "INDX", "IBSD", "BDRX", "IFIX"
    ]

    try:
        # Extrai a composição da carteira dos índices setoriais
        carteira_extractor = extract_composicao_da_carteira_indices_setoriais.Extract(path_data_raw, indices)
        carteira_extractor.execute()

        # Extrai e salva informações dos índices
        informacoes_extractor = extract_informacoes_dos_indices.Extract(path_data_raw, indices)
        informacoes_extractor.get_and_save_informacoes_indice()

    except Exception as e:
        print(f"Ocorreu um erro durante a execução: {e}")