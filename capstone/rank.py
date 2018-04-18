import pandas as pd
import numpy as np
from sklearn import svm
from sklearn import tree
from sklearn.linear_model import LogisticRegression as lr
import graphviz
import nltk
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
import json
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import KFold
import pickle
from capstone.store import *
from capstone.config import *

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def ruleBasedSearch(sentenceList):
    # return new dataframe, colName: to be, other verb, verb, punctuation, pronoun
    newPd = pd.DataFrame(columns=['toBe','defVerb','verb','punctuation','pronoun'])
    for sen in sentenceList:
        #print(sen)
        result = [0]*5
        # tobe
        reTOBE = re.compile(r'\b(be|is|are|was|were|being|={1})\b', flags=re.IGNORECASE)
        if (reTOBE.findall(sen)!=[]):
            result[0] = 1
        # defVerb
        reDefVerb = re.compile(r'\b(as|define|defines|defined|mean|means|meant|refer|refers|referred{1})\b', flags=re.IGNORECASE)
        if (reDefVerb.findall(sen)!=[]):
            result[1] = 1
        # punctuation
        rePunc = re.compile(r'(:|-|\()')
        if (rePunc.findall(sen)!=[]):
            result[3] = 1


        tokens = nltk.word_tokenize(sen)
        tagged = nltk.pos_tag(tokens)
        #print(tagged)

        tagged_text_string = " ".join(["{}/{}".format(word,pos) for word, pos in tagged])
        try:
           gold_chunked_text = tagstr2tree(tagged_text_string)
        except ValueError:
            # a math equation is included as text
            newPd.loc[len(newPd)] = result
            continue

        unchunked_text = gold_chunked_text.flatten()

        # verb
        chunk_rule = ChunkRule("<VB|VBG|VBD|VBN|VBP|VBZ>", "Chunk verb")
        chunk_parser = RegexpChunkParser([chunk_rule], chunk_label='NP')
        chunked_text = chunk_parser.parse(unchunked_text)
        #print(chunked_text)
        if (chunked_text.height()>=3):
            result[2] = 1
        # pronoun
        chunk_rule1 = ChunkRule("<PRP|PRP\$>", "Chunk pronoun")
        chunk_parser1 = RegexpChunkParser([chunk_rule1], chunk_label='NP')
        chunked_text1 = chunk_parser1.parse(unchunked_text)
        if (chunked_text1.height()>=3):
            result[4] = 1

        """
        posTag = ' '.join(pos for _,pos in nltk.pos_tag(nltk.word_tokenize(sen)))
        print(posTag)
        # verb
        reVerb = re.compile(r'(VB?)', flags=re.IGNORECASE)
        if (reVerb.findall(sen)!=[]):
            result[2] = 1
        # pronoun
        rePronoun = re.compile(r'(PRP)', flags=re.IGNORECASE)
        if (rePronoun.findall(sen)!=[]):
            result[4] = 1
        """
        newPd.loc[len(newPd)] = result
    return newPd


# process sentence tagged as "text", replace math expressions with different tokens
# if the math expression contains the symbol of interest, replace with TARGET
# else, replace with MATH
def token_math(sentence, symbol):

    expres = []
    splits = sentence.split("$")

    for idx in range(len(splits)):
        if idx % 2 == 1:
            expres.append(splits[idx])

            if symbol in splits[idx]:
                splits[idx] = "TARGET"
            else:
                splits[idx] = 'MATH'

    return ''.join(splits), expres



def equationSide(math, symbol):
#     output: 0 - no equal sign
#         1 - target symbol on right-hand side
#         2 - target symbol on left-hand side
    segment = math.split("=")
    if (len(segment)==1):
        # no = sign
        return 0
    if (symbol in segment[0]):
        # appear on lhs
        for i in range(1,len(segment)):
            # both on lhs & rhs
            if (symbol in segment[i]):
                return 0
        return 2
    for i in range(1,len(segment)):
        if (symbol in segment[i]):
            return 1
    return 0

def getEquationSide(mathSegment, symbol):
    label = []
    for math in mathSegment:
        label.append(equationSide(math, symbol))
    return max(label)


def get_data(sentence):
#     input: sentenceFile: list of parsed sentence file
#             paperFile: name of all the paper sentences
    #df = pd.DataFrame(columns=["sentence", "position", "numAppearance", "label"])
    table = []
    #paper = json.load(open(paperFile)) #!!!!!!!!!!!!!!!!!!!!!!!!
    paper = load_from_file(file_format='json', filename=json_output_filename)


    # load sentence json
    #sentence = json.load(open(senFile))
    docname = sentence["doc_name"]
    symbolExpr = sentence["symbol_expr"]
    sentences = sentence["sentences"]
    totalAppearance = len(sentences)
    # get total number of sentences in that paper
    totalSentenceLen = len(paper[docname])
    totalSentence = paper[docname][totalSentenceLen-1]["sentence_idx"]+1
    firstAppearanceSentenceIndex = sentences[0]["sentence_idx"]

    for i in range(len(sentences)):
        if (sentences[i]["type"]=="text"):
            precessedSen, mathSegment = token_math(sentences[i]["expr"], symbolExpr.strip())
            equLabel = getEquationSide(mathSegment, symbolExpr.strip())
        elif (sentences[i]["type"]=="math"):
            precessedSen = sentences[i]["expr"]
            equLabel = getEquationSide([precessedSen], symbolExpr)
        else:
            print("Unknown type label when parsing the file:"+sentences[i]["type"])
            continue

        temp = [precessedSen, len(sentences[i]["expr"]), sentences[i]["sentence_idx"]/totalSentence, (i+1)/totalAppearance, equLabel, (sentences[i]["sentence_idx"]-firstAppearanceSentenceIndex)/totalSentence ,0]
        if (sentences[i]["label"]=="definition"):
            temp[6] = 1
        elif (sentences[i]["label"]=="usecase"):
            temp[6] = 1
        #print(temp)
        table.append(temp)

    df = pd.DataFrame(table, columns=["sentence", "len","position", "numAppearance", "rhsOrlhs","distanceToFirstAppearance","label"])
    #print(df)

    # get sentence structure attributes
    vec = ruleBasedSearch(df[df.columns[0]].tolist())
    df = pd.concat([df,vec], axis=1)
    #print(df)
    print(df.shape)
    return df

def prob_predict(pre, threshold = 0.5):
    result = [0]*len(pre)

    for i in range(len(pre)):
        if pre[i][1]>= threshold:
            result[i] = 1
    return result

def rank(sentence, algoName = 'ML' , prob = True, threshold = 0.5):
    df = get_data(sentence)

    # generate training data and labels
    X = df[['len','position', 'numAppearance','rhsOrlhs','toBe','defVerb','verb','punctuation','pronoun','distanceToFirstAppearance']]
    #Y = df['label']
    model = pickle.load(open(model_filename, 'rb'))
    if (prob):
        #pred = prob_predict(model.predict_proba(X), threshold=threshold)
        pred = model.predict_proba(X)
    else:
        pred = model.predict(X)
    # get ranking
    # if (algoName=='RF' or prob):
    #     rank = pred
    # else:
    #     rank = np.array(pred[:,1])
    rank = np.array(pred[:,1])
    sort_index = np.argsort(-1*rank)
    ranked_sentences = []
    for j in sort_index:
        ranked_sentences.append(sentence["sentences"][j])

    return ranked_sentences
