
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

options = webdriver.ChromeOptions()


with webdriver.Chrome(options=options) as driver:

    url = 'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/search?language=pt-br'

    driver.get(url)

    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'div')))

    rows = driver.find_elements(By.CSS_SELECTOR, 'div')
    lista = []
    for row in rows:
        try:
            lista.append(row.find_element(By.CLASS_NAME, 'card-title2').text)
        except:
            pass

    lista = list(set(lista))
    print(lista)

    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="nav-bloco"]/div/div[1]/div/div')))    
    element.click() 
    sleep(10)

    link_page = driver.current_url
    print(link_page)

    sleep(5)

    driver.back()

    sleep(5)

    
    # PASSAR PARA A PROXIMA PAGINA
    # sleep(5)
    # button_pass = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="listing_pagination"]/pagination-template/ul/li[10]/a')))    
    # button_pass.click()         
    # sleep(5)

    # print(set(lista))