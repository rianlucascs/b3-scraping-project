import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import config

class ExtractAndTransform:

    def __init__(self, path_processed_data, url, headers):
        self.path_processed_data = path_processed_data
        self.url = url
        self.headers = headers
    
    def extract(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tabela = soup.find('table')
        dados = []
        for tr in tabela.find_all('tr')[1:]:  
            linha = [td.get_text(strip=True) for td in tr.find_all('td')]
            if linha: 
                dados.append(linha)
        return dados

    def transform(self, extract_data):
        df_data = DataFrame(extract_data, columns=self.headers)
        return df_data
    
    def save(self, df_data):
        df_data.to_csv(self.path_processed_data, index=False, encoding='utf-8')

    def run(self):
        extract_data = self.extract()
        transform_data = self.transform(extract_data)
        self.save(transform_data)

if __name__ == '__main__':
    extract_and_transform = ExtractAndTransform(
        config.path_processed_data, 
        config.url,
        config.headers
        )
    extract_and_transform.run()
    