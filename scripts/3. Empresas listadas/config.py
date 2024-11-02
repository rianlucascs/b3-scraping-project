from os.path import join, dirname, abspath
from selenium.webdriver.chrome.options import Options

path_extracted_data = join(dirname(dirname(dirname(abspath(__file__)))), 'extracted_data', '3. Empresas listadas')

path_processed_data = join(dirname(dirname(dirname(abspath(__file__)))), 'processed_data', '3. Empresas listadas')

url = 'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/search?language=pt-br'

options = Options()
options.add_argument("--start-maximized") 
options.add_argument("--disable-infobars")  
options.add_argument("--disable-extensions")  
options.add_argument("--incognito")  
options.add_argument("--disable-gpu")  
options.add_argument("--no-sandbox")  
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36") 
        