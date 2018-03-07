from capstone.util import *
from capstone.preprocess import *

def main():
    print('starting main ...')
    html_file = load_html_file('data/html_files/transfer_learning/output.html')
    for p in html_file.find_all('p'):
        for c in p.children:
            print(c)

if __name__ == '__main__':
    main()
