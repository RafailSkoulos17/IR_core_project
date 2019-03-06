import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT,ID
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
import sys

data = open_dir("indexdir")  # open index dir
q_str = "GAME"  # query name
limiter = 10   # number of results


with data.searcher(weighting=scoring.TF_IDF) as searcher:
       query = QueryParser("content", data.schema).parse(q_str)
      # query = MultifieldParser(["title", "content"], data.schema).parse(q_str)
       results = searcher.search(query, limit = limiter)
       for i in range(limiter):
           print(results[i]['title'], str(results[i].score), results[i]['doc'])
