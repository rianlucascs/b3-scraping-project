from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
from os.path import join

class Extract:

    def __init__(self, path_extracted_data):
        self.path_extracted_data = path_extracted_data
        pass
    
    def get_codigos_page(self, driver:webdriver.Chrome) -> list:
        rows = driver.find_elements(By.CLASS_NAME, 'card-title2')
        lista = []
        for row in rows:
            lista.append(row.text)
        print()
        return list(set(lista))

    def get_quantidade_de_paginas(self, driver:webdriver.Chrome):
        return int(driver.find_element(By.XPATH, '//*[@id="listing_pagination"]/pagination-template/ul/li[9]/a/span[2]').text)

    def driver_page(self):
        url = 'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/search?language=pt-br'

        options = webdriver.ChromeOptions()

        with webdriver.Chrome(options=options) as driver:
            driver.get(url)
            for i in list(range(1, self.get_quantidade_de_paginas(driver))):
                

            codigos_page = self.get_codigos_page(driver)

            print(self.get_quantidade_de_paginas(driver))

            

if __name__ == '__main__':
    
    extract = Extract().driver_page()
