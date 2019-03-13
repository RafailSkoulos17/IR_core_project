from copy import copy

from trec_car import read_data
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import math
from gensim.summarization.bm25 import get_bm25_weights
from math import exp, expm1





f = open("queries/queries.txt", "r")
contents =f.read()


def write_to_file(label, headline, qid, para_text, doc_id, f):

    f.write(b" id =   " + bytes(str(id), 'utf8') + b"        para =   " + bytes(str(para_text), 'utf8') +  b"\n")



def hierarchical_iter_sections(section, headline, f, qlist, label):
    headline += '/' + section.heading
    for part in section.children:
        if isinstance(part, read_data.Para):
            para_text = part.get_text()
            if bytes(str(headline).replace("/", " "), 'utf8') not in qlist:
                # i += 1
                write_to_file(label, headline, len(qlist) + 1, para_text, part.paragraph.para_id, f)
                qlist += [bytes(str(para_text).replace("/", " "), 'utf8')]
        elif isinstance(part, read_data.Section):
            hierarchical_iter_sections(part, headline, f, qlist, label)


def build_hierarchical():
    # read_file = r'benchmarkY1/benchmarkY1-train/train.pages.cbor'
    read_file = r'test200/test200-train/train.pages.cbor'
    write_file = 'queries/paragraphs.txt'
    qlist = []
    label = 1
    with open(write_file, 'wb') as f:
        for page in read_data.iter_pages(open(read_file, 'rb')):
            for part in page.skeleton:
                if isinstance(part, read_data.Para):
                    headline = page.page_name
                    page_text = part.get_text()
                    if bytes(str(headline).replace("/", " "), 'utf8') not in qlist:
                        # i += 1
                        write_to_file(label, headline, len(qlist) + 1, page_text, part.paragraph.para_id, f)
                        qlist += [bytes(str(page_text).replace("/", " "), 'utf8')]
                elif isinstance(part, read_data.Section):
                    headline = page.page_name
                    # i += 1
                    hierarchical_iter_sections(part, headline, f, qlist, label)
                    # print(i)

i = 0
build_hierarchical()
