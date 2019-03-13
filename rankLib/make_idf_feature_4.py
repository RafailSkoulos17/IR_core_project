from copy import copy

from trec_car import read_data
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import math
from gensim.summarization.bm25 import get_bm25_weights
from math import exp, expm1
import json

d2 = {}
iterations = 0

def remove_string_special_characters(s):
    # Replace special characters
    stripped = re.sub('[^\w\s]', ' ', s)
    stripped = re.sub('_', '', stripped)

    # Change any whitespace to one space
    stripped = re.sub('\s',' ', stripped)

    # Remove start and end wihte spaces
    stripped = stripped.strip()

    return stripped



def idf_of_body():
    global d2
    global iterations
    d = {}
    paragraphs = open("queries/paragraphs.txt", "r")
    paragraphs = paragraphs.readlines()
    queries = open("queries/queries.txt", "r").readlines()
    write_file = 'queries/idf_representation.txt'
    with open(write_file, 'wb') as f:
        count_list = []
        iter = 0
        for line in queries:
            counts = 0
            line_queries = line
            iter += 1
            line_queries2 = remove_string_special_characters(line_queries)
            iter_para = 0
            for line_paragraphs in paragraphs:
                line_paragraphs2 = remove_string_special_characters(line_paragraphs)
                iter_para += 1
                for i in line_queries2.split():
                    if line_paragraphs2.count(i):
                        counts = counts + 1
            if counts > 0:  #>>>>>>>>>>>>problem with zero division<<<<<<<<<<<<<
                count_list += [math.log10(iter_para/counts)]
                idf_score = math.log10(iter_para / counts)
            d = {'qid': iter, 'idf_score': idf_score}
            d2[iterations] = d
            iterations += 1


idf_of_body()

with open('queries/data_2.json', 'w') as fp:
    json.dump(d2, fp)