from os.path import join, dirname, abspath
from selenium.webdriver.chrome.options import Options

# Caminhos para os diretórios de dados extraídos e processados
path_extracted_data = join(dirname(dirname(dirname(abspath(__file__)))), 'extracted_data', '3. Empresas listadas')
path_processed_data = join(dirname(dirname(dirname(abspath(__file__)))), 'processed_data', '3. Empresas listadas')

# URL da página de listagem de empresas na B3
url = 'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/search?language=pt-br'

# Configurações do Selenium para o navegador Chrome
options = Options()
options.add_argument("--start-maximized")  # Inicia o navegador em modo maximizado
options.add_argument("--disable-infobars")  # Desabilita a barra de informações
options.add_argument("--disable-extensions")  # Desabilita as extensões do navegador
options.add_argument("--incognito")  # Inicia o navegador em modo de navegação anônima
options.add_argument("--disable-gpu")  # Desabilita a aceleração de GPU (útil em ambientes sem interface gráfica)
options.add_argument("--no-sandbox")  # Desabilita o sandboxing (necessário em alguns ambientes)
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")  # Define o user agent