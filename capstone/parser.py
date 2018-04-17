from .util import *
from .config import *

def parse_to_array(html_path, math_len_limit=3, text_len_limit=5):
    html_file = load_html_file(html_path)
    word_cnt = 0
    sentence_cnt = 0
    sentences = []
    raw_sentences = []
    str_word_cnt = 0
    str_sentence_cnt = 0
    for seg in html_file.find_all(include_tags):
        if seg.name == 'math':
            str_seg = ''
            for agg_str in seg.stripped_strings:
                str_seg += agg_str
            if len(str_seg) > text_len_limit:
                raw_sentences.append({
                    'str': str_seg,
                    'word_idx': str_word_cnt,
                    'sentence_idx': str_word_cnt,
                    'label': 'unlabeled'
                })
            str_word_cnt = str_sentence_cnt + 1
            str_word_cnt = str_word_cnt + len(str_seg)
        else:
            full_str = ''
            for agg_str in seg.stripped_strings:
                full_str += agg_str
            for str_seg in full_str.split('.'):
                if len(str_seg) > text_len_limit:
                    raw_sentences.append({
                        'str': str_seg,
                        'word_idx': str_word_cnt,
                        'sentence_idx': str_word_cnt,
                        'label': 'unlabeled'
                    })
                str_word_cnt = str_sentence_cnt + 1
                str_word_cnt = str_word_cnt + len(str_seg)
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
    return sentences, raw_sentences
