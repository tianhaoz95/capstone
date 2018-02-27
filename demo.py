from capstone.util import *

def main():
    print('starting main ...')
    # convert_tex_to_html('data/tex_files/faster_rcnn/rpn_pami_arxiv.tex', 'data/xml_files/faster_rcnn/output.xml')
    html_file = load_html_file('data/html_files/faster_rcnn/output.html')
    for seg in html_file.find_all('math'):
        print(seg['alttext'])

if __name__ == '__main__':
    main()
