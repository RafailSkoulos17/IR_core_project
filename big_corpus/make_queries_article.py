import json

from trec_car import read_data

types = ["article", "toplevel", "hierarchical"]


def make_queries(t):
    queries_dict = {
        "index": "C:/IR_core_project/indexes/corpus_index_dir",
        "queryType": "structured",
        "verbose": True,
        "requested": 20,
        "processingModel": "org.lemurproject.galago.core.retrieval.processing.RankedDocumentModel",
        "scorer": "bm25",
        "k": 1.2,
        "b": 0.75
    }
    fin = "../train.v2.0.tar/train/base.train.cbor-outlines.cbor"
    queries_dict['queries'] = []
    i = 0
    for s in read_data.iter_annotations(open(fin, 'rb')):
        q = s.page_name
        if q:
            queries_dict['queries'] += [{"number": "enwiki:" + str(q.rstrip().replace(" ", "%20")),
                                         "text": "#combine(" + q.rstrip().replace("/", " ") + ")"}]

    with open('jsons/' + t + '_queries_for_galago_search.json', "w") as fout:
        json.dump(queries_dict, fout)


def make_queries_with_expansion(t):
    queries_dict = {
        "index": "C:/IR_core_project/indexes/corpus_index_dir",
        "queryType": "structured",
        "verbose": True,
        "requested": 20,
        "operatorWrap": "rm",
        "relevanceModel": "org.lemurproject.galago.core.retrieval.prf.RelevanceModel1",
        "fbDocs": 10,
        "fbTerm": 30,
        "extentQuery": True,
        # "fbOrigWeight": 0.5,
        "rmstopwords": "rmstop",
        "processingModel": "org.lemurproject.galago.core.retrieval.processing.RankedDocumentModel",
        "scorer": "bm25",
        "k": 1.2,
        "b": 0.75
    }
    fin = "../train.v2.0.tar/train/base.train.cbor-outlines.cbor"
    queries_dict['queries'] = []
    i = 0
    for s in read_data.iter_annotations(open(fin, 'rb')):
        q = s.page_name
        if q:
            queries_dict['queries'] += [{"number": "enwiki:" + str(q.rstrip().replace(" ", "%20")),
                                         "text": "#combine(" + q.rstrip().replace("/", " ") + ")"}]

    with open('jsons/' + t + 'expanded_rm1_' + t + '_queries_for_galago_search.json', "w") as fout:
        json.dump(queries_dict, fout)



#
def make_queries_with_expansion_rm3(t):
    queries_dict = {
        "index": "C:/IR_core_project/indexes/corpus_index_dir",
        "queryType": "structured",
        "verbose": True,
        "requested": 20,
        "operatorWrap": "rm",
        "relevanceModel": "org.lemurproject.galago.core.retrieval.prf.RelevanceModel3",
        "fbDocs": 10,
        "fbTerm": 30,
        "extentQuery": True,
        "fbOrigWeight": 0.5,
        "rmstopwords": "rmstop",
        "processingModel": "org.lemurproject.galago.core.retrieval.processing.RankedDocumentModel",
        "scorer": "bm25",
        "k": 1.2,
        "b": 0.75
    }

    fin = "../train.v2.0.tar/train/base.train.cbor-outlines.cbor"
    queries_dict['queries'] = []
    i = 0
    for s in read_data.iter_annotations(open(fin, 'rb')):
        q = s.page_name
        if q:
            queries_dict['queries'] += [{"number": "enwiki:" + str(q.rstrip().replace(" ", "%20")),
                                         "text": "#combine(" + q.rstrip().replace("/", " ") + ")"}]
    with open('jsons/' + t + 'expanded_rm3_queries_for_galago_search.json', "w") as fout:
        json.dump(queries_dict, fout)


if __name__ == '__main__':
    make_queries('article')
    make_queries_with_expansion('article')
    make_queries_with_expansion_rm3('article')




