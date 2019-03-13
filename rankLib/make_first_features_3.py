from trec_car import read_data
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import math
from gensim.summarization.bm25 import get_bm25_weights
import json


i = 0
d2 = {}
d_qrels = {}

def write_to_file(label, headline, qid, para_text, doc_id, f, dl_body, dl_anchor, tf, tf_anchor, idf_relevant):
    global i
    global d2
    global d_qrels
    d = {}
    d_q = {}

    d = {'relevant': label, 'qid': qid, 'dl': dl_body, 'dl_anchor': dl_anchor, 'tf': tf, 'idf_per_para' : idf_relevant, 'para_id': doc_id}
    d2[i] = d
    d_q = {'qid': qid, 'para_id': doc_id,'relevant': label}
    d_qrels[i] = d_q
    i += 1
    # print(d)






def hierarchical_iter_sections(section, headline, f, qlist, label):
    headline += '/' + section.heading
    for part in section.children:
        # i += 1
        if isinstance(part, read_data.Para):
            # page_text = part[0].get_text()
            page_text = part.get_text()
            if bytes(str(headline).replace("/", " "), 'utf8') not in qlist:
                dl_body = document_length_body(page_text)
                dl_anchor = document_length_anchor(part)
                tf_acnhor = tf_anchor(part, headline)
                tf = TF_IDF(page_text, headline)
                idf_score = idf_of_body(page_text, headline)
                write_to_file(label, headline, len(qlist) + 1, page_text, part.paragraph.para_id, f, dl_body, dl_anchor, tf, tf_acnhor, idf_score)
                qlist += [bytes(str(headline).replace("/", " "), 'utf8')]
            else:
                dl_body = document_length_body(page_text)
                dl_anchor = document_length_anchor(part)
                tf_acnhor = tf_anchor(part, headline)
                tf = TF_IDF(page_text, headline)
                idf_score = idf_of_body(page_text, headline)
                write_to_file(label, headline, len(qlist), page_text, part.paragraph.para_id, f, dl_body, dl_anchor, tf, tf_acnhor, idf_score)
        elif isinstance(part, read_data.Section):
            hierarchical_iter_sections(part, headline, f, qlist, label)


def build_hierarchical():
    # read_file = r'benchmarkY1/benchmarkY1-train/train.pages.cbor'
    read_file = r'test200/test200-train/train.pages.cbor'
    write_file = 'queries/RankLib_representation.txt'
    qlist = []
    label = 1
    with open(write_file, 'wb') as f:
        i = 0
        for page in read_data.iter_pages(open(read_file, 'rb')):
            # i += 1
            for part in page.skeleton:
                if isinstance(part, read_data.Para):
                    headline = page.page_name
                    page_text = part.get_text()
                    if bytes(str(headline).replace("/", " "), 'utf8') not in qlist:
                        dl_body = document_length_body(page_text)
                        dl_anchor = document_length_anchor(part)
                        tf_acnhor = tf_anchor(part, headline)
                        tf = TF_IDF(page_text, headline)
                        idf_score = idf_of_body(page_text, headline)
                        write_to_file(label, headline, len(qlist) + 1, page_text, part.paragraph.para_id, f, dl_body, dl_anchor, tf, tf_acnhor, idf_score,)
                        qlist += [bytes(str(headline).replace("/", " "), 'utf8')]
                    else:
                        dl_body = document_length_body(page_text)
                        dl_anchor = document_length_anchor(part)
                        tf_acnhor = tf_anchor(part, headline)
                        tf = TF_IDF(page_text, headline)
                        idf_score = idf_of_body(page_text, headline)
                        write_to_file(label, headline, len(qlist), page_text, part.paragraph.para_id, f, dl_body, dl_anchor, tf, tf_acnhor, idf_score)
                elif isinstance(part, read_data.Section):
                    headline = page.page_name
                    hierarchical_iter_sections(part, headline, f, qlist, label)


# Function that calculated the document length

def document_length_body(page_text):
    for char in '-.,\n':
        Text = page_text.replace(char, ' ')
    Text = Text.lower()
    word_list = Text.split()
    # print(len(word_list))
    return len(word_list)


# Function that calculated the anchor's length

def document_length_anchor(para):
    # if isinstance(page, read_data.Para):
    length = 0
    for i in para.paragraph.bodies:
        if isinstance(i, read_data.ParaLink):
            length = length + 1
            # print(i.anchor_text)
    # print(length)
    return(length)

# Function that calculates the tf of the anchor
def tf_anchor(para, headline):
    text = " "
    white_space = " "
    for i in para.paragraph.bodies:
        if isinstance(i, read_data.ParaLink):
            text = text + white_space+ i.anchor_text
            # print(i.anchor_text)
    # print(text)
    TF_IDF(text, headline)

# Function that calculates the idf of the a pair
def idf_of_body(para, headline):
    count = 0
    # print(para)
    # print(headline.replace("/", " "))
    headline = remove_string_special_characters(headline)
    for i in headline.split():
        # print(i)
        # print(headline)
        # if not para.count(i):
        #     count = 0
        if para.count(i):
            count = count + 1
    return count
    # print(count)

# Not used

def TF_IDF(paragraph, headline):
    white_space = " "
    text_sents = [headline + white_space + paragraph]
    text_sents_clean = [remove_string_special_characters(s) for s in text_sents]
    doc_info = get_doc(text_sents_clean)

    text_sents_headline = [headline]
    text_sents_clean_headline = [remove_string_special_characters(s) for s in text_sents_headline]
    freqDict_list_headline = create_freq_dict(text_sents_clean_headline)

    freqDict_list = create_freq_dict(text_sents_clean)
    TF_scores = computeTF(doc_info, freqDict_list)
    # IDF_scores = computeIDF(doc_info, freqDict_list)
    # TFIDF_scores = computeTFIDF(TF_scores, IDF_scores)

    TF_sum = 0
    for words in range(len(freqDict_list_headline[0]['freq_dict'])):
            TF_sum = TF_sum + TF_scores[words]['TF_score']
    return TF_sum

# Function that removes the special character from the query or the paragraph

def remove_string_special_characters(s):
    # Replace special characters
    stripped = re.sub('[^\w\s]', ' ', s)
    stripped = re.sub('_', '', stripped)

    # Change any whitespace to one space
    stripped = re.sub('\s',' ', stripped)

    # Remove start and end wihte spaces
    stripped = stripped.strip()

    return stripped

def get_doc(sent):
    doc_info = []
    i = 0
    for sent in sent:
        i += 1
        count = count_words(sent)
        temp = {'doc_id' : i, 'doc_length' : count}
        doc_info.append(temp)
    return doc_info

def count_words(sent):
    count = 0
    words = word_tokenize(sent)
    for word in words:
        count += 1
    return count

def create_freq_dict(sents):
    i = 0
    freqDict_list = []
    for sent in sents:
        i += 1
        freq_dict = {}
        words = word_tokenize(sent)
        for word in words:
            word = word.lower()
            if word in freq_dict:
                freq_dict[word] += 1
            else:
                freq_dict[word] = 1
        temp = {'doc_id' : i, 'freq_dict': freq_dict}
        freqDict_list.append(temp)
    return freqDict_list


def computeTF(doc_info, freqDict_list):
    TF_scores = []
    for tempDict in freqDict_list:
        id = tempDict['doc_id']
        for k in tempDict['freq_dict']:
            temp = {'doc_id': id,
                    'TF_score' : tempDict['freq_dict'][k]/doc_info[id-1]['doc_length'],
                    'key' : k}

            TF_scores.append(temp)
    return TF_scores


def computeIDF(doc_info, freqDict_list):
    IDF_scores = []
    counter = 0
    for dict in freqDict_list:
        counter += 1
        for k in dict['freq_dict'].keys():
            count = sum([k in tempDict['freq_dict'] for tempDict in freqDict_list])
            temp = {'doc_id' : counter, 'IDF_score' : math.log(len(doc_info)/count), 'key' : k}

            IDF_scores.append(temp)
    return IDF_scores

def computeTFIDF(TF_scores, IDF_scores):
    TFIDF_scores = []
    for j in IDF_scores:
        for i in TF_scores:
            if j['key'] == i['key'] and j['doc_id'] == i['doc_id']:
                temp = {'doc_id' : j['doc_id'],
                        'TFIDF_score' : j['IDF_score']*i['TF_score'],
                        'key' : i['key']}
        TFIDF_scores.append(temp)
    return TFIDF_scores

build_hierarchical()

with open('queries/data_1.json', 'w') as fp:
    json.dump(d2, fp)

with open('queries/data_qrels.json', 'w') as fp:
    json.dump(d_qrels, fp)