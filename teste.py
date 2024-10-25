with open(r'C:\Users\xxis4\Desktop\b3-scraping-project\extracted_data\3. Empresas listadas\paginas\n_page_1\Códigos_page.txt', 'r', encoding='utf-8') as f:
    file = eval(f.read())

print([f for f in file if 'ABCC' in f][0])