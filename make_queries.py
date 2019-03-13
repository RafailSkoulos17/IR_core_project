from trec_car import read_data


def write_to_file(headline, f):
    f.write(bytes(str(headline), 'utf8'))
    f.write(b'\n')


def hierarchical_iter_sections(section, headline, f, qlist):
    headline += '/' + section.heading
    for part in section.children:
        if isinstance(part, read_data.Para):
            if headline not in qlist:
                write_to_file(headline, f)
                qlist += [headline]
        elif isinstance(part, read_data.Section):
            hierarchical_iter_sections(part, headline, f, qlist)


def toplevel_iter_sections(section, headline, f, qlist):
    for part in section.children:
        if isinstance(part, read_data.Para):
            if headline not in qlist:
                write_to_file(headline, f)
                qlist += [headline]
        elif isinstance(part, read_data.Section):
            article_iter_sections(part, headline, f, qlist)


def article_iter_sections(section, headline, f,qlist):
    for part in section.children:
        if isinstance(part, read_data.Para):
            if headline not in qlist:
                write_to_file(headline, f)
                qlist += [headline]
        elif isinstance(part, read_data.Section):
            article_iter_sections(part, headline, f, qlist)


def build_article():
    # read_file = r'benchmarkY1\benchmarkY1-train\train.pages.cbor'
    read_file = r'test200-train\train.pages.cbor'
    write_file = 'queries/article.txt'
    qlist = []
    with open(write_file, 'wb') as f:
        for page in read_data.iter_pages(open(read_file, 'rb')):
            headline = page.page_name
            for part in page.skeleton:
                if isinstance(part, read_data.Para):
                    if headline not in qlist:
                        write_to_file(headline, f)
                        qlist += [headline]
                elif isinstance(part, read_data.Section):
                    article_iter_sections(part, headline, f, qlist)


def build_hierarchical():
    # read_file = r'benchmarkY1\benchmarkY1-train\train.pages.cbor'
    read_file = r'test200-train\train.pages.cbor'
    write_file = 'queries/hierarchical.txt'
    qlist = []
    with open(write_file, 'wb') as f:
        for page in read_data.iter_pages(open(read_file, 'rb')):
            for part in page.skeleton:
                if isinstance(part, read_data.Para):
                    headline = page.page_name
                    if headline not in qlist:
                        write_to_file(headline, f)
                        qlist += [headline]
                elif isinstance(part, read_data.Section):
                    headline = page.page_name
                    hierarchical_iter_sections(part, headline, f, qlist)


def build_toplevel():
    # read_file = r'benchmarkY1\benchmarkY1-train\train.pages.cbor'
    read_file = r'test200-train\train.pages.cbor'
    write_file = 'queries/toplevel.txt'
    qlist = []

    with open(write_file, 'wb') as f:
        for page in read_data.iter_pages(open(read_file, 'rb')):
            for part in page.skeleton:
                if isinstance(part, read_data.Para):
                    headline = page.page_name
                    if headline not in qlist:
                        write_to_file(headline, f)
                        qlist += [headline]
                elif isinstance(part, read_data.Section):
                    headline = str(page.page_name) + '/' + str(part.heading)
                    toplevel_iter_sections(part, headline, f, qlist)


build_article()
build_hierarchical()
build_toplevel()
