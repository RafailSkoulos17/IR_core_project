import json

from trec_car import read_data


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


    queries_dict_rm1 = {
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

    queries_dict_rm3 = {
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

    queries_dict['queries'] = []
    queries_dict_rm1['queries'] = []
    queries_dict_rm3['queries'] = []

    fin = "../train.v2.0.tar/train/base.train.cbor-outlines.cbor"

    for p in read_data.iter_outlines(open(fin, 'rb')):
        if len(p.outline()) > 2:
            queries = ["/".join([str(section.heading) for section in sectionpath]) for sectionpath in p.flat_headings_list()]

            pn = p.page_name

            queries_dict['queries'] += [{"number": "enwiki:" + str(pn.rstrip().replace(" ", "%20")),
                                         "text": "#combine(" + pn.rstrip().replace("/", " ") + ")"}]

            queries_dict_rm1['queries'] += [{"number": "enwiki:" + str(pn.rstrip().replace(" ", "%20")),
                                             "text": "#combine(" + pn.rstrip().replace("/", " ") + ")"}]

            queries_dict_rm3['queries'] += [{"number": "enwiki:" + str(pn.rstrip().replace(" ", "%20")),
                                             "text": "#combine(" + pn.rstrip().replace("/", " ") + ")"}]

            for q in queries:
                q = str(pn.rstrip().replace(" ", "%20")) + "/" + q
                queries_dict['queries'] += [{"number": "enwiki:" + str(q.rstrip().replace(" ", "%20")),
                                                     "text": "#combine(" + q.rstrip().replace("/", " ") + ")"}]

                queries_dict_rm1['queries'] += [{"number": "enwiki:" + str(q.rstrip().replace(" ", "%20")),
                                             "text": "#combine(" + q.rstrip().replace("/", " ") + ")"}]

                queries_dict_rm3['queries'] += [{"number": "enwiki:" + str(q.rstrip().replace(" ", "%20")),
                                             "text": "#combine(" + q.rstrip().replace("/", " ") + ")"}]

    with open('jsons/' + t + '_queries_for_galago_search.json', "w") as fout:
        json.dump(queries_dict, fout)

    with open('jsons/' + t + 'expanded_rm1_queries_for_galago_search.json', "w") as fout:
        json.dump(queries_dict_rm1, fout)

    with open('jsons/' + t + 'expanded_rm3_queries_for_galago_search.json', "w") as fout:
        json.dump(queries_dict_rm3, fout)



if __name__ == '__main__':
    make_queries('hierarchical')





