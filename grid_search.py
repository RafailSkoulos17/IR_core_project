import json

types = ["article", "toplevel", "hierarchical"]

def make_queries(t):
    with open("queries/" + t + ".txt", "rb") as fin:
        queries_dict = {
            "index": "C:/IR_core_project/indexes/corpus_index_dir",
            "queryType": "structured",
            "verbose": True,
            "requested": 20,
            # "operatorWrap": "rm",
            # "relevanceModel": "org.lemurproject.galago.core.retrieval.prf.RelevanceModel1",
            # "fbDocs": 10,
            # "fbTerm": 10,
            "processingModel": "org.lemurproject.galago.core.retrieval.processing.RankedDocumentModel",
            "scorer": "bm25",
            "k": 1.2,
            "b": 0.75
        }
        queries_dict['queries'] = []
        i = 0
        for q in fin.readlines():
            q = q.decode('utf8')
            if q:
                queries_dict['queries'] += [{"number": "enwiki:" + str(q.rstrip().replace(" ", "%20")),
                                             "text": "#combine(" + q.rstrip().replace("/", " ") + ")"}]

    with open('galago_jsons/' + t + '_queries_for_galago_search.json', "w") as fout:
        json.dump(queries_dict, fout)


def make_queries_with_expansion(t, fbDoc, fbTerm):
    with open("queries/" + t + ".txt", "rb") as fin:
        queries_dict = {
            "index": "C:/IR_core_project/indexes/corpus_index_dir",
            "queryType": "structured",
            "verbose": True,
            "requested": 20,
            "operatorWrap": "rm",
            "relevanceModel": "org.lemurproject.galago.core.retrieval.prf.RelevanceModel1",
            "fbDocs": fbDoc,
            "fbTerm": fbTerm,
            "extentQuery": True,
            # "fbOrigWeight": 0.5,
            "rmstopwords": "rmstop",
            "processingModel": "org.lemurproject.galago.core.retrieval.processing.RankedDocumentModel",
            "scorer": "bm25",
            "k": 1.2,
            "b": 0.75
        }
        queries_dict['queries'] = []
        i = 0
        for q in fin.readlines():
            q = q.decode('utf8')
            if q:
                queries_dict['queries'] += [{"number": "enwiki:" + str(q.rstrip().replace(" ", "%20")),
                                             "text": "#combine(" + q.rstrip().replace("/", " ") + ")"}]

    with open('galago_jsons/expanded_rm1_' + t + "_" + str(fbDoc) + "_" + str(fbTerm)  + "_"+ '_queries_for_galago_search.json', "w") as fout:
        json.dump(queries_dict, fout)


def make_queries_with_expansion_rm3(t, fbDoc, fbTerm, fbOrigWeight):
    with open("queries/" + t + ".txt", "rb") as fin:
        queries_dict = {
            "index": "C:/IR_core_project/indexes/corpus_index_dir",
            "queryType": "structured",
            "verbose": True,
            "requested": 20,
            "operatorWrap": "rm",
            "relevanceModel": "org.lemurproject.galago.core.retrieval.prf.RelevanceModel3",
            "fbDocs": fbDoc,
            "fbTerm": fbTerm,
            "extentQuery": True,
            "fbOrigWeight": fbOrigWeight,
            "rmstopwords": "rmstop",
            "processingModel": "org.lemurproject.galago.core.retrieval.processing.RankedDocumentModel",
            "scorer": "bm25",
            "k": 1.2,
            "b": 0.75
        }
        queries_dict['queries'] = []
        i = 0
        for q in fin.readlines():
            q = q.decode('utf8')
            if q:
                queries_dict['queries'] += [{"number": "enwiki:" + str(q.rstrip().replace(" ", "%20")),
                                             "text": "#combine(" + q.rstrip().replace("/", " ") + ")"}]

    with open('galago_jsons/expanded_rm3_' + t + "_" + str(fbDoc) + "_" + str(fbTerm) + "_"+ str(fbOrigWeight) + "_"+ '_queries_for_galago_search.json', "w") as fout:
        json.dump(queries_dict, fout)


fbDocs = [5, 10, 25, 20]
fbTerms = [5, 10, 15, 20, 25, 30]
fbOrigWeights = [0.2, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8]
if __name__ == '__main__':
    for t in types:
        for fbDoc in fbDocs:
            for fbTerm in fbTerms:
                for fbOrigWeight in fbOrigWeights:
                    make_queries_with_expansion_rm3(t, fbDoc, fbTerm, fbOrigWeight)
                make_queries_with_expansion(t,fbDoc, fbTerm)
        make_queries(t)




