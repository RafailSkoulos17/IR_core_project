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


data = open_dir("indexdir")  # open index dir
q_str = "Political status of Transnistria"  # query name
limiter = 10   # number of results


with data.searcher(weighting=TF_IDF) as searcher:
       query = QueryParser("content", data.schema, group=OrGroup).parse(q_str)
      # query = MultifieldParser(["title", "content"], data.schema).parse(q_str)
       results = searcher.search(query, limit=limiter)
       for i in range(len(results.top_n)):
           print(q_str, str(results[i].score), results[i]['doc'])
