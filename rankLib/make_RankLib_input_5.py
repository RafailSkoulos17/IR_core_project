import json
import random
from gensim.summarization.bm25 import get_bm25_weights
from gensim import models
import re
from nltk.tokenize import word_tokenize, sent_tokenize
import math



with open('queries/data_2.json', 'r') as fp:
    d1 = json.load(fp)

with open('queries/data_1.json', 'r') as fp:
    d2 = json.load(fp)


# BM 25 feature extraction


queries = open("queries/queries.txt", "r")
queries = queries.readlines()

paragraphs = open("queries/paragraphs.txt", "r")
paragraphs = paragraphs.readlines()
whitespace = " "
iter = 0
bm25_score = {}

i = 0
j = 0

query = queries[0].split()
for line in paragraphs:
    line2 = line.split()
    if d2[str(i)]['qid'] == d1[str(j)]['qid']:
        query = queries[j].split()
        j += 1
    corpus = [query, line2]
    result = get_bm25_weights(corpus)
    maximum = result[0][1]
    bm25_score[i] = {'qid': j, 'score' : maximum}
    i += 1


i = 0
j = 0

for line in range(len(d2)):
    # print(d2[i])
    if d2[str(i)]['qid'] != d1[str(j)]['qid']:
        # d2[i].update(d1[j]['qid'])
        j += 1
    d2[str(i)].update({'idf': d1[str(j)]['idf_score']})
    d2[str(i)].update({'tfidf': float(d2[str(i)]['tf'])*float(d2[str(i)]['idf'])})
    d2[str(i)].update({'bm25_score': float(bm25_score[i]['score'])})
    i += 1

# dictionary with the sequence of every paragraph

i = 0
j = 0
sum = 0
query_list_seq = {}
for query in range(len(d2)):
    sum += 1
    if d2[str(query)]['qid'] != d1[str(j)]['qid']:
        j += 1
        sum = 1
    query_list_seq[j] = {'qid': j+1, 'seq' : sum}

#Function that calculates the document length

def document_length_body(page_text):
    for char in '-.,\n':
        Text = page_text.replace(char, ' ')
    Text = Text.lower()
    word_list = Text.split()
    return len(word_list)


# Function that calculates the idf of a pair
def idf_of_body(para, headline):
    count = 0
    headline = remove_string_special_characters(headline)
    for i in headline.split():
        if para.count(i):
            count = count + 1
    return count

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

    TF_sum = 0
    for words in range(len(freqDict_list_headline[0]['freq_dict'])):
            TF_sum = TF_sum + TF_scores[words]['TF_score']
    return TF_sum

# Function that removes the special characters
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

#fucntion that creates a dicitonary with the frequence of the same pairs

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


# making the non relevant query-paragraph pairs

i = 0
j = 0
non_relevant = {}
non_relevant_qrels = {}
for line in queries:

    for seq in range(query_list_seq[j]['seq']):
        par = random.randint(1, len(paragraphs)-1)
        dl = document_length_body(paragraphs[par])
        dl_anchor = random.randint(1, 5)
        tf = TF_IDF(paragraphs[par], line)
        idf_score = idf_of_body(paragraphs, line)
        corpus = [paragraphs[par].split(), line.split()]
        result = get_bm25_weights(corpus)
        bm_maximum = result[0][1]
        non_relevant[i] = {'relevant': 0,  'qid': j+1, 'dl': dl, 'dl_anchor': dl_anchor, 'tf': tf, 'idf_per_para': idf_score, 'bm25_score': bm_maximum, 'para_id': i+1}
        non_relevant_qrels[i] = {'qid': j+1, 'para_id': i+1,'relevant': 0}
        i += 1
    j += 1

with open('queries/data_qrels_non_relevant.json', 'w') as fp:
    json.dump(non_relevant_qrels, fp)


for line in range(len(non_relevant)):
    idf = str(d2[str(line)]['idf'])
    tfidf = str(float(d2[str(line)]['idf'])*float(non_relevant[line]['tf']))
    non_relevant[line].update({'idf': idf})
    non_relevant[line].update({'tfidf': tfidf})


relevant = d2
concatenated = {}
concatenated_qrels = {}




with open('queries/data_qrels.json', 'r') as fp:
    relevant_qrels = json.load(fp)



k = 0
count = 0
count_r = 0
count_n = 0
for i in range(len(d1)):
        for j in range(query_list_seq[i]['seq']):
            concatenated[str(count)] = relevant[str(count_r)]
            concatenated_qrels[str(count)] = relevant_qrels[str(count_r)]
            count += 1
            count_r += 1
        for k in range(query_list_seq[i]['seq']):
            concatenated[str(count)] = non_relevant[count_n]
            concatenated_qrels[str(count)] = non_relevant_qrels[count_n]
            count += 1
            count_n += 1

with open('queries/data_qrels_concatenated.json', 'w') as fp:
    json.dump(concatenated_qrels, fp)

fout = "queries/RankLib_input.txt"
with open(fout, 'wb') as f:
    for line in range(len(concatenated)):
        relevant = str(concatenated[str(line)]['relevant'])
        qid = str(concatenated[str(line)]['qid'])
        dl = str(concatenated[str(line)]['dl'])
        dl_anchor = str(concatenated[str(line)]['dl_anchor'])
        tf = str(concatenated[str(line)]['tf'])
        idf = str(concatenated[str(line)]['idf'])
        tfidf = str(concatenated[str(line)]['tfidf'])
        idf_per_para = str(concatenated[str(line)]['idf_per_para'])
        para_id  = str(concatenated[str(line)]['para_id'])
        bm25_score = str(concatenated[str(line)]['bm25_score'])
        f.write(b" " + bytes(str(relevant), 'utf8')
                + b" qid:" + bytes(str(qid), 'utf8')
                + b" 1:" + bytes(str(dl), 'utf8')
                + b" 2:" + bytes(str(dl_anchor), 'utf8')
                + b" 3:" + bytes(str(tf), 'utf8')
                + b" 4:" + bytes(str(idf), 'utf8')
                + b" 5:" + bytes(str(tfidf), 'utf8')
                + b" 6:" + bytes(str(idf_per_para), 'utf8')
                + b" 7:" + bytes(str(bm25_score), 'utf8')
                + b" #docid:" + bytes(str(para_id), 'utf8') + b"\n")

fout = "queries/RankLib_input_attributes.txt"
with open(fout, 'wb') as f:
    for line in range(len(concatenated)):
        relevant = str(concatenated[str(line)]['relevant'])
        qid = str(concatenated[str(line)]['qid'])
        dl = str(concatenated[str(line)]['dl'])
        dl_anchor = str(concatenated[str(line)]['dl_anchor'])
        tf = str(concatenated[str(line)]['tf'])
        idf = str(concatenated[str(line)]['idf'])
        tfidf = str(concatenated[str(line)]['tfidf'])
        idf_per_para = str(concatenated[str(line)]['idf_per_para'])
        para_id = str(concatenated[str(line)]['para_id'])
        bm25_score = str(concatenated[str(line)]['bm25_score'])
        f.write(b" " + bytes(str(relevant), 'utf8')
                + b"    qid:  " + bytes(str(qid), 'utf8')
                + b"    document length:    " + bytes(str(dl), 'utf8')
                + b"    anchor length:  " + bytes(str(dl_anchor), 'utf8')
                + b"    TF: " + bytes(str(tf), 'utf8')
                + b"    IDF:   " + bytes(str(idf), 'utf8')
                + b"    TF-IDF: " + bytes(str(tfidf), 'utf8')
                + b"    IDF per paragraph:  " + bytes(str(idf_per_para), 'utf8')
                + b"    bm score:   " + bytes(str(bm25_score), 'utf8')
                + b"    #docid: " + bytes(str(para_id), 'utf8') + b"\n")

# fout = "queries/RankLib_input_positive.txt"
# with open(fout, 'wb') as f:
#     for line in range(len(concatenated)):
#         relevant = str(concatenated[str(line)]['relevant'])
#         qid = str(concatenated[str(line)]['qid'])
#         dl = str(concatenated[str(line)]['dl'])
#         dl_anchor = str(concatenated[str(line)]['dl_anchor'])
#         tf = str(concatenated[str(line)]['tf'])
#         idf = math.fabs(float(str(concatenated[str(line)]['idf'])))
#         tfidf = math.fabs(float(str(concatenated[str(line)]['tfidf'])))
#         idf_per_para = math.fabs(float(str(concatenated[str(line)]['idf_per_para'])))
#         para_id = str(concatenated[str(line)]['para_id'])
#         bm25_score = math.fabs(float(str(concatenated[str(line)]['bm25_score'])))
#         f.write(b" " + bytes(str(relevant), 'utf8')
#                 + b" qid:" + bytes(str(qid), 'utf8')
#                 + b" 1:" + bytes(str(dl), 'utf8')
#                 + b" 2:" + bytes(str(dl_anchor), 'utf8')
#                 + b" 3:" + bytes(str(tf), 'utf8')
#                 + b" 4:" + bytes(str(idf), 'utf8')
#                 + b" 5:" + bytes(str(tfidf), 'utf8')
#                 + b" 6:" + bytes(str(idf_per_para), 'utf8')
#                 + b" 7:" + bytes(str(bm25_score), 'utf8')
#                 + b" #docid:" + bytes(str(para_id), 'utf8') + b"\n")

fout = "queries/RankLib_input_relevant.txt"
with open(fout, 'wb') as f:
    for line in range(len(d2)):
        relevant = str(d2[str(line)]['relevant'])
        qid = str(d2[str(line)]['qid'])
        dl = str(d2[str(line)]['dl'])
        dl_anchor = str(d2[str(line)]['dl_anchor'])
        tf = str(d2[str(line)]['tf'])
        idf = str(d2[str(line)]['idf'])
        tfidf = str(d2[str(line)]['tfidf'])
        idf_per_para = str(d2[str(line)]['idf_per_para'])
        para_id  = str(d2[str(line)]['para_id'])
        bm25_score = str(d2[str(line)]['bm25_score'])
        f.write(b" " + bytes(str(relevant), 'utf8')
                + b" qid:" + bytes(str(qid), 'utf8')
                + b" 1:" + bytes(str(dl), 'utf8')
                + b" 2:" + bytes(str(dl_anchor), 'utf8')
                + b" 3:" + bytes(str(tf), 'utf8')
                + b" 4:" + bytes(str(idf), 'utf8')
                + b" 5:" + bytes(str(tfidf), 'utf8')
                + b" 6:" + bytes(str(idf_per_para), 'utf8')
                + b" 7:" + bytes(str(bm25_score), 'utf8')
                + b" #docid:" + bytes(str(para_id), 'utf8') + b"\n")

fout = "queries/RankLib_qrels_input.txt"
with open(fout, 'wb') as f:
    for line in range(len(concatenated_qrels)):
        qid =  str(concatenated_qrels[str(line)]['qid'])
        doc_id = str(concatenated_qrels[str(line)]['para_id'])
        label = str(concatenated_qrels[str(line)]['relevant'])
        f.write(bytes(str(qid), 'utf8') + b" QO " + bytes(str(doc_id), 'utf8') + b" " + bytes(str(label), 'utf8') + b"\n")