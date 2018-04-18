from flask import Flask
from flask import render_template
from flask import request
from threading import Thread
from capstone.store import *
from capstone.config import *
from capstone.util import *
from capstone.rank import *
import webbrowser
import time
import numpy

url = 'http://127.0.0.1:5000/'

app = Flask(__name__)

dataset = load_from_file(file_format='json', filename=json_output_filename)

current_doc_name = None

current_symbol_expr = None

symbol_detector = SymbolDetector(symlist_filename=symlist_filename)

@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template('home_page.html')
    return render_template('error.html')

@app.route('/search', methods=['POST', 'GET'])
def searching():
    doc_list = dataset.keys()
    if request.method == 'GET':
        return render_template('search.html', sentence_list=[], doc_list=doc_list)
    if request.method == 'POST':
        doc_name = request.form['doc_name']
        symbol_expr = request.form['symbol_expr']
        code, filtered_sentences = filter_by_doc_symbol(dataset=dataset,
            symbol_detector=symbol_detector, doc_name=doc_name, symbol_expr=symbol_expr)
        if code == 'success':
            senFile = {
                'doc_name': doc_name,
                'symbol_expr': symbol_expr,
                'sentences': filtered_sentences,
            }
            ranked_sentences = rank(senFile, algoName = 'ML' ,prob = True, threshold = 0.45)
            return render_template('search.html', sentence_list=ranked_sentences, doc_list=doc_list, doc_name=doc_name, symbol_expr=symbol_expr)
        if code == 'symbol_not_exist':
            return render_template('search.html', sentence_list=[], doc_list=doc_list, doc_name=doc_name, symbol_expr=symbol_expr)
    return render_template('error.html')

@app.route('/label', methods=['POST', 'GET'])
def label():
    global current_doc_name
    global current_symbol_expr
    if request.method == 'GET':
        return render_template('label_tools.html', sentence_list=[])
    if request.method == 'POST':
        action_type = request.form['btn_name']
        if action_type == 'search':
            doc_name = request.form['doc_name']
            current_doc_name = doc_name
            symbol_expr = request.form['symbol_expr']
            current_symbol_expr = symbol_expr
            code, filtered_sentences = filter_by_doc_symbol(dataset=dataset,
                symbol_detector=symbol_detector, doc_name=doc_name, symbol_expr=symbol_expr)
            if code == 'success':
                return render_template('label_tools.html', sentence_list=filtered_sentences)
            if code == 'symbol_not_exist':
                return render_template('label_tools.html', sentence_list=[])
        if action_type == 'save_overall':
            data = dict(request.form)
            del data['btn_name']
            for key, val in data.items():
                idx = int(key)
                label = val
                dataset[current_doc_name][idx]['label'] = label[0]
            save_to_file(file_format='json', filename=json_output_filename, data=dataset)
            return render_template('label_tools.html', sentence_list=[])
        if action_type == 'save_separate':
            data = dict(request.form)
            del data['btn_name']
            output_sentences = []
            for key, val in data.items():
                idx = int(key)
                label = val
                sentence = dataset[current_doc_name][idx]
                sentence['label'] = label[0]
                output_sentences.append(sentence)
            output_data = {
                'doc_name': current_doc_name,
                'symbol_expr': current_symbol_expr,
                'sentences': output_sentences
            }
            symbol_field = current_symbol_expr
            symbol_field = symbol_field.replace('\\', '')
            output_filename = output_root + '/' + current_doc_name + '_' + symbol_field + '.json'
            save_to_file(file_format='json', filename=output_filename, data=output_data)
            return render_template('label_tools.html', sentence_list=[])
        if action_type == 'save_both':
            data = dict(request.form)
            del data['btn_name']
            for key, val in data.items():
                idx = int(key)
                label = val
                dataset[current_doc_name][idx]['label'] = label[0]
            save_to_file(file_format='json', filename=json_output_filename, data=dataset)
            output_sentences = []
            for key, val in data.items():
                idx = int(key)
                label = val
                sentence = dataset[current_doc_name][idx]
                sentence['label'] = label[0]
                output_sentences.append(sentence)
            output_data = {
                'doc_name': current_doc_name,
                'symbol_expr': current_symbol_expr,
                'sentences': output_sentences
            }
            symbol_field = current_symbol_expr
            symbol_field = symbol_field.replace('\\', '')
            output_filename = output_root + '/' + current_doc_name + '_' + symbol_field + '.json'
            save_to_file(file_format='json', filename=output_filename, data=output_data)
            return render_template('label_tools.html', sentence_list=[])
        return render_template('error.html')

def open_browser():
    print('Starting browser ...')
    time.sleep(1)
    webbrowser.open_new(url)

if __name__ == '__main__':
    browser_t = Thread(target=open_browser)
    browser_t.start()
    app.run()
