import os
import subprocess as sp
import pandas as pd
from bs4 import BeautifulSoup

def list_tex_dest_paths(root):
    html_root = root + '/html_files'
    tex_root = root + '/tex_files'
    raw_tex_names = os.listdir(tex_root)
    tex_names = []
    for raw_tex_name in raw_tex_names:
        if os.path.isdir(tex_root + '/' + raw_tex_name):
            tex_names.append(raw_tex_name)
    tex_paths = [tex_root + '/' + tex_name for tex_name in tex_names]
    html_paths = [html_root + '/' + tex_name for tex_name in tex_names]
    html_filenames = [html_root + '/' + tex_name + '/output.html' for tex_name in tex_names]
    tex_filenames = []
    for tex_path in tex_paths:
        filenames = os.listdir(tex_path)
        tex_filename = tex_path
        if 'main.tex' in filenames:
            tex_filename = tex_filename + '/main.tex'
        else:
            for filename in filenames:
                if '.tex' in filename:
                    tex_filename = tex_filename + '/' + filename
        tex_filenames.append(tex_filename)
    return tex_filenames, html_filenames, tex_paths, html_paths, tex_names

def convert_tex_to_html(tex_path, dest_path):
    test_commands = [
        'latexml',
        '--VERSION'
    ]
    convert_commands = [
        'latexml',
        tex_path
    ]
    output_commands = [
        'latexmlpost',
        '--dest=' + dest_path,
        '-'
    ]
    proc = None
    proc = sp.Popen(test_commands)
    proc = sp.Popen(convert_commands, stdout=sp.PIPE)
    proc = sp.Popen(output_commands, stdin=proc.stdout)
    proc.communicate()
    print('conversion finished')

def load_html_file(filename):
    soup = None
    with open(filename) as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
    return soup

def extract_elements(html_file, handlers):
    tags = html_file.find_all(handlers.keys())
    outputs = []
    for tag in tags:
        handler = handlers[tag.name]
        output = handler(tag)
        outputs.extend(output)
    return outputs

def extract_features(elements, handlers, dest_path=None):
    output = {}
    output['plain_sentences'] = elements
    for handler_name, handler in handler.items():
        features = handler(elements)
        output[handler_name] = features
    output_df = pd.DataFrame(output)
    if dest_path:
        output_df.to_csv(dest_path)
    return output_df

class SymbolDetector():

    def __init__(self, symlist_filename):
        symbol_list = []
        if symlist_filename:
            with open(symlist_filename, 'r') as f:
                symbol_list = f.read().split()
        self.symbol_list = symbol_list

    def find_similar_symbols(self, symbol_in):
        similar_symbols = []
        size = len(symbol_in)
        for s in self.symbol_list:
            if len(s) > len(symbol_in) and s[:size] == symbol_in:
                similar_symbols.append(s)
        return similar_symbols

    def scan_sentence(self, sentence, target_symbol):
        if len(sentence) < len(target_symbol):
            return False
        for i in range(len(sentence) - len(target_symbol)):
            seg = sentence[i:i + len(target_symbol)]
            if seg == target_symbol:
                return True
        return False

    def scan_words(self, sentence, target_symbol):
        words = sentence.split()
        for word in words:
            if word == target_symbol:
                return True
        return False

    def detect_symbol(self, sentence, target_symbol):
        if self.scan_words(sentence, target_symbol):
            return True
        similar_symbols = self.find_similar_symbols(target_symbol)
        for similar_symbol in similar_symbols:
            if self.scan_sentence(sentence, similar_symbol):
                return False
        return self.scan_sentence(sentence, target_symbol)

    def detect_symbols(self, sentence, target_symbols):
        for target_symbol in target_symbols:
            if self.detect_symbol(sentence, target_symbol):
                return True
        return False
