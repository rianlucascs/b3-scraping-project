from yfinance import download
import config
from os.path import join
from pandas import read_csv


class CheckExistsSerieTemporal:
     
    def __init__(self, path_processed_data):
        self.path_processed_data = path_processed_data
    
    def check(self, list_data):
        try:
            for i, ticker in enumerate(list_data):
                df_data = download(f'{ticker}.SA', period='max', progress=False)
                
        except:
            pass

    def run(self):
        list_data = list(read_csv(join(self.path_processed_data, 'todas_empresas_listadas.csv'), sep=';')['codigo'])
        self.check(list_data)
        


if __name__ == '__main__':
    
    check = CheckExistsSerieTemporal(config.path_processed_data)
    check.run()
