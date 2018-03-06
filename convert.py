from capstone.util import *
from capstone.preprocess import *
from capstone.parser import *
from capstone.store import *

def main():
    print('start converting ...')
    tex_filenames, html_filenames, tex_paths, html_paths, tex_names = preprocess_tex_files()
    size = len(html_filenames)
    res_dict = {}
    for i in range(size):
        sentences = parse_to_array(html_filenames[i])
        res_dict[tex_names[i]] = sentences
    save_to_file(file_format='json', filename='data/json_files/output.json', data=res_dict)

if __name__ == '__main__':
    main()
