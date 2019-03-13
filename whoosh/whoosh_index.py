import os
import re
from whoosh.fields import Schema, ID, KEYWORD, TEXT
from whoosh.index import create_in
from whoosh.query import Term

data = "index_inputs/hierarchical_index.trectext"

schema = Schema(content=TEXT, doc=ID(stored=True))  # Define schema

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

ix = create_in("indexdir", schema)
writer = ix.writer()

intext = False
doc_pattern = '<DOCNO> (.*) <\/DOCNO>'
headline_pattern = '<HEADLINE> (.*) <\/HEADLINE>'
text = ""


#fileobj = open(data, "r")

with open(data, "r", encoding="utf8") as f:
        for line in f.readlines():
            if line.startswith("</TEXT>"):
                intext = False
                new_text = text
                text = ""
            elif intext:
                text += line
            elif line.startswith("</DOC>"):
                writer.add_document(content=new_text,doc=docno)
                print(docno, headline, new_text)
            elif line.startswith("<DOCNO>"):
                docno = re.search(doc_pattern, line).group(1)
                # docno = doc_pattern.findall(line)
            elif line.startswith("<HEADLINE>"):
                headline = re.search(headline_pattern, line).group(1)
                # headline = headline_pattern.findall(line)
            elif line.startswith("<TEXT>"):
                intext = True
        writer.commit()