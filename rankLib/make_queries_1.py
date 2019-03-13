from trec_car import read_data


def write_to_file(headline, qid, f):
    # f.write(bytes(str(headline).replace("/", " "), 'utf8') + b"|" + bytes(str(qid), 'utf8') + b"\n")
    f.write(bytes(str(headline).replace("/", " "), 'utf8') + b"\n")


def hierarchical_iter_sections(section, headline, f, qlist):
    headline += '/' + section.heading
    for part in section.children:
        if isinstance(part, read_data.Para):
            if bytes(str(headline).replace("/", " "), 'utf8') not in qlist:
                write_to_file(headline, len(qlist) + 1, f)
                qlist += [bytes(str(headline).replace("/", " "), 'utf8')]
        elif isinstance(part, read_data.Section):
            hierarchical_iter_sections(part, headline, f, qlist)


def build_hierarchical():
    # read_file = r'benchmarkY1/benchmarkY1-train/train.pages.cbor'
    read_file = r'test200/test200-train/train.pages.cbor'
    write_file = 'queries/queries.txt'
    qlist = []
    with open(write_file, 'wb') as f:
        for page in read_data.iter_pages(open(read_file, 'rb')):
            for part in page.skeleton:
                if isinstance(part, read_data.Para):
                    headline = page.page_name
                    if bytes(str(headline).replace("/", " "), 'utf8') not in qlist:
                        write_to_file(headline, len(qlist) + 1, f)
                        qlist += [bytes(str(headline).replace("/", " "), 'utf8')]
                elif isinstance(part, read_data.Section):
                    headline = page.page_name
                    hierarchical_iter_sections(part, headline, f, qlist)


build_hierarchical()
