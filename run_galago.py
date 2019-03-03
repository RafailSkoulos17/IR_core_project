import subprocess
from subprocess import check_output
import re

subprocess.run(["C:/IR_core_project/galago-3.15-bin/bin/galago", "build",
                "C:/IR_core_project/myBuildFile.json"],
               stderr=subprocess.STDOUT, shell=True)
out = check_output(["C:/IR_core_project/galago-3.15-bin/bin/galago", "get-rm-terms",
                    "C:/IR_core_project/myQueryExpansionFile.json"],
                   stderr=subprocess.STDOUT, shell=True)
out = out.decode("utf-8")

p = re.compile('\n(.*)\t')
terms = p.findall(out)
print(terms)

