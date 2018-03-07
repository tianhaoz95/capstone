from flask import Flask
from flask import render_template
from flask import request
from capstone.store import *
from capstone.config import *
from capstone.util import *
app = Flask(__name__)

dataset = load_from_file(file_format='json', filename=json_output_filename)

symbol_detector = SymbolDetector(symlist_filename=symlist_filename)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'GET':
        return render_template('label_tools.html',
                sentence_list=[])
    if request.method == 'POST':
        print(request.form)
        action_type = request.form['btn_name']
        if action_type == 'search':
            doc_name = request.form['doc_name']
            symbol_expr = request.form['symbol_expr']
            code, filtered_sentences = filter_by_doc_symbol(dataset=dataset,
                symbol_detector=symbol_detector, doc_name=doc_name, symbol_expr=symbol_expr)
            print(filtered_sentences)
            if code == 'success':
                return render_template('label_tools.html',
                        sentence_list=filtered_sentences,
                        show_modify_btn=True)
            if code == 'symbol_not_exist':
                return render_template('label_tools.html',
                        sentence_list=[])
        return code
