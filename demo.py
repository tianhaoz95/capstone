from capstone.util import *

def main():
    print('starting main ...')
    convert_tex_to_html('data/tex_files/faster_rcnn/rpn_pami_arxiv.tex', 'data/xml_files/faster_rcnn/output.xml')
    # html_file = load_html_file('data/xml_files/faster_rcnn/output.xml')

if __name__ == '__main__':
    main()
