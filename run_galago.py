import subprocess
import sys
from subprocess import check_output, Popen
import re
from make_queries_for_galago_search import make_queries, make_queries_with_expansion, make_queries_with_expansion_rm3

# build = Popen(["C:/IR_core_project/galago-3.15-bin/bin/galago", "build",
#                "galago_jsons/myBuildFile.json"],
#                shell=True)
# build.wait()
# query_expansion_results = check_output(["C:/IR_core_project/galago-3.15-bin/bin/galago", "get-rm-terms",
#                                         "C:/IR_core_project/myQueryExpansionFile.json"],
#                                        stderr=subprocess.STDOUT, shell=True)
# query_expansion_results = query_expansion_results.decode("utf-8")
#
# p = re.compile('\n(.*)\t')
# terms = p.findall(query_expansion_results)
# print(terms)
#

# types = ["article", "toplevel", "hierarchical"]
# for t in types:
#
#     make_queries(t)
#     make_queries_with_expansion(t)
#     make_queries_with_expansion_rm3(t)


    # search_results = open('trec_eval/runfiles/' + t, 'w', encoding="utf8")
    #
    # search = Popen(["C:/IR_core_project/galago-3.15-bin/bin/galago", "batch-search",
    #                 "galago_jsons/" + t +"_queries_for_galago_search.json"],
    #                 stdout=subprocess.PIPE, shell=True)
    #
    # for index, line in enumerate(search.stdout):
    #     search_results.write(line.decode('utf8').rstrip())
    #     # if index != len(search.stdout) -1:
    #     search_results.write("\n")
    # search.wait()
    #
trec_eval_results = open('big_corpus/results/rm1_hierarchical.eval', 'w', encoding="utf8")
trec_eval = Popen([r"trec_eval\trec_eval", "-q", "trec_eval/qrels/train.pages.cbor-hierarchical.qrels",
                   "galago-3.15-bin/bin/expanded_rm1_hierarchical_runfile"],
                   stdout=subprocess.PIPE, shell=True)

for line in trec_eval.stdout:
    # sys.stdout.write(line.decode('utf8'))
    trec_eval_results.write(line.decode('utf8'))
trec_eval.wait()
    #
    #
    # # ------------------------------------expanded RM1---------------------------------------
    #
    #
    # search_results = open('trec_eval/runfiles/expanded_' + t, 'w', encoding="utf8")
    #
    # search = Popen(["C:/IR_core_project/galago-3.15-bin/bin/galago", "batch-search",
    #                 "galago_jsons/expanded_" + t + "_queries_for_galago_search.json"],
    #                stdout=subprocess.PIPE, shell=True)
    #
    # for index, line in enumerate(search.stdout):
    #     search_results.write(line.decode('utf8').rstrip())
    #     # if index != len(search.stdout) -1:
    #     search_results.write("\n")
    # search.wait()
    #
    # trec_eval_results = open('trec_eval/results/expanded_' + t + '.eval', 'w', encoding="utf8")
    # trec_eval = Popen([r"trec_eval\trec_eval", "-q", "trec_eval/qrels/train.pages.cbor-" + t + ".qrels",
    #                    "trec_eval/runfiles/expanded_" + t],
    #                   stdout=subprocess.PIPE, shell=True)
    #
    # for line in trec_eval.stdout:
    #     # sys.stdout.write(line.decode('utf8'))
    #     trec_eval_results.write(line.decode('utf8'))
    # trec_eval.wait()

    # ------------------------------------expanded RM3---------------------------------------

    # search_results = open('trec_eval/runfiles/expanded_rm3_' + t, 'w', encoding="utf8")
    #
    # search = Popen(["C:/IR_core_project/galago-3.15-bin/bin/galago", "batch-search",
    #                 "galago_jsons/expanded_rm3_" + t + "_queries_for_galago_search.json"],
    #                stdout=subprocess.PIPE, shell=True)
    #
    # for index, line in enumerate(search.stdout):
    #     search_results.write(line.decode('utf8').rstrip())
    #     # if index != len(search.stdout) -1:
    #     search_results.write("\n")
    # search.wait()

    # trec_eval_results = open('trec_eval/results/expanded_rm3_' + t + '.eval', 'w', encoding="utf8")
    # trec_eval = Popen([r"trec_eval\trec_eval", "-q", "trec_eval/qrels/train.pages.cbor-" + t + ".qrels",
    #                    "trec_eval/runfiles/expanded_rm3_" + t],
    #                   stdout=subprocess.PIPE, shell=True)
    #
    # for line in trec_eval.stdout:
    #     # sys.stdout.write(line.decode('utf8'))
    #     trec_eval_results.write(line.decode('utf8'))
    # trec_eval.wait()