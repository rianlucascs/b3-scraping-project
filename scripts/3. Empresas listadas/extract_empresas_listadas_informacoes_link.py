
import config
from os import listdir
from os.path import join

class Extract:

    def __init__(self, path_extracted_data):
        self.path_extracted_data = path_extracted_data
        self.dir_page = join(self.path_extracted_data, 'paginas')

    
    def get_qtd_pages(self) -> int:
        return len(listdir(self.dir_page))
    
    def run():
        pass

if __name__ == '__main__':

    extract = Extract(config.path_extracted_data)
    print(extract.get_qtd_pages())

    