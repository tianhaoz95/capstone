from capstone.util import *

def main():
    print('starting main ...')
    # convert_tex_to_html('data/tex_files/faster_rcnn/rpn_pami_arxiv.tex', 'data/html_files/faster_rcnn/output.html')
    html_file = load_html_file('data/html_files/faster_rcnn/output.html')
    for it in html_file.find_all(['p', 'math']):
        print(it.contents)

if __name__ == '__main__':
    main()
