import os
import re

from whoosh.scoring import WeightingModel, TF_IDF, BM25F, WeightScorer, WeightLengthScorer
from whoosh.scoring import Weighting
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT,ID
from whoosh.qparser import QueryParser, OrGroup
from whoosh import scoring
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
import sys
from math import log, sqrt

data_2 = open("C:\\Users\\Kon\\Documents\\Python\\temp\\queries.txt", encoding='utf-8')
query_strings=[]
for line in data_2:
    line1 = line.split('|')[0]
    query_strings.append(line1)

data = open_dir("indexdir")  # open index dir
#q_str = list  # query name
limiter = 10  # number of results


with data.searcher(weighting = scoring.TF_IDF) as searcher:
    for query_string in query_strings:
        query = QueryParser("content", data.schema, group=qparser.OrGroup).parse(query_string)
        # query = MultifieldParser(["title", "content"], data.schema).parse(query_string)
        results = searcher.search(query, limit = limiter)
        matched_docs = []
        for i in range(limiter):
            try:
               
                print(query_string, str(results[i].score), results[i]['doc'])
            except IndexError:
                pass
