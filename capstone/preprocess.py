from .util import *
import shutil

def preprocess_tex_files():
    tex_filenames, html_filenames, tex_paths, html_paths, tex_names = list_tex_dest_paths('data')
    for i, tex_filename in enumerate(tex_filenames):
        print('converting ', tex_filename, '...')
        # convert_tex_to_html(tex_filename, html_filenames[i])
    for html_path, tex_name in zip(html_paths, tex_names):
        convert_html_file(html_path)
    return tex_filenames, html_filenames, tex_paths, html_paths, tex_names
