from .util import *
from .config import *

def parse_to_array(html_path, math_len_limit=3, text_len_limit=5):
    html_file = load_html_file(html_path)
    word_cnt = 0
    sentence_cnt = 0
    sentences = []
    for seg in html_file.find_all(include_tags):
        if seg.name == 'math':
            expr = seg['alttext']
            if len(expr) >= math_len_limit:
                elt = {
                    'type': 'math',
                    'expr': '$$' + expr + '$$',
                    'word_idx': word_cnt,
                    'sentence_idx': sentence_cnt,
                    'label': 'unlabeled'
                }
                sentences.append(elt)
                word_cnt += len(expr)
                sentence_cnt += 1
        else:
            seg_expr = ''
            for segc in seg.children:
                if segc.name == 'math':
                    math_expr = segc['alttext'].replace('.', '')
                    expr = '$' + math_expr + '$'
                else:
                    expr = segc.string
                if expr and expr != '\n' and expr != '$$' and expr != '$\n$':
                    seg_expr = seg_expr + ' ' + expr
            exprs = seg_expr.strip().split('.')
            for expr in exprs:
                if len(expr) >= text_len_limit:
                    elt = {
                        'type': 'text',
                        'expr': expr,
                        'word_idx': word_cnt,
                        'sentence_idx': sentence_cnt,
                        'label': 'unlabeled'
                    }
                    sentences.append(elt)
                    word_cnt += len(expr)
                    sentence_cnt += 1
    return sentences
