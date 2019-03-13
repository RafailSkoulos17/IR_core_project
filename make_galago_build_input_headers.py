from trec_car import read_data


def write_to_file(text, para_id, headline, f):
    f.write(b'<DOC>\n')
    f.write(b'<DOCNO> ' + bytes(str(para_id), 'utf8') + b' </DOCNO>\n')
    f.write(b'<HEADLINE> ' + bytes(str(headline), 'utf8') + b' </HEADLINE>\n')
    text = (text).encode('utf8')
    f.write(b'<TEXT>\n')
    f.write(text)
    f.write(b'\n</TEXT>\n')
    f.write(b'</DOC>\n')


def hierarchical_iter_sections(section, headline, f, qlist):
    headline += '/' + section.heading
    for part in section.children:
        if isinstance(part, read_data.Para):
            para_text = part.get_text()
            if part.paragraph.para_id not in qlist:
                write_to_file(para_text, part.paragraph.para_id, headline, f)
                qlist += [part.paragraph.para_id]
        elif isinstance(part, read_data.Section):
            hierarchical_iter_sections(part, headline, f, qlist)


def toplevel_iter_sections(section, headline, f):
    for part in section.children:
        if isinstance(part, read_data.Para):
            para_text = part.get_text()
            write_to_file(para_text, part.paragraph.para_id, headline, f)
        elif isinstance(part, read_data.Section):
            article_iter_sections(part, headline, f)


def article_iter_sections(section, headline, f):
    for part in section.children:
        if isinstance(part, read_data.Para):
            para_text = part.get_text()
            write_to_file(para_text, part.paragraph.para_id, headline, f)
        elif isinstance(part, read_data.Section):
            article_iter_sections(part, headline, f)


def build_article():
    # read_file = r'benchmarkY1\benchmarkY1-train\train.pages.cbor'
    read_file = r'test200-train\train.pages.cbor'
    write_file = 'index_inputs/article_index.trectext'
    with open(write_file, 'wb') as f:
        for page in read_data.iter_pages(open(read_file, 'rb')):
            headline = page.page_name
            for part in page.skeleton:
                if isinstance(part, read_data.Para):
                    page_text = part.get_text()
                    write_to_file(page_text, part.paragraph.para_id, headline, f)
                elif isinstance(part, read_data.Section):
                    article_iter_sections(part, headline, f)


def build_hierarchical():
    # read_file = r'benchmarkY1\benchmarkY1-train\train.pages.cbor'
    read_file = r'test200-train\train.pages.cbor'
    write_file = 'index_inputs/hierarchical_index.trectext'
    qlist = []
    with open(write_file, 'wb') as f:
        for page in read_data.iter_pages(open(read_file, 'rb')):
            for part in page.skeleton:
                if isinstance(part, read_data.Para):
                    page_text = part.get_text()
                    headline = page.page_name
                    if part.paragraph.para_id not in qlist:
                        write_to_file(page_text, part.paragraph.para_id, headline, f)
                        qlist += [part.paragraph.para_id]
                elif isinstance(part, read_data.Section):
                    headline = page.page_name
                    hierarchical_iter_sections(part, headline, f, qlist)


def build_toplevel():
    # read_file = r'benchmarkY1\benchmarkY1-train\train.pages.cbor'
    read_file = r'test200-train\train.pages.cbor'
    write_file = 'index_inputs/toplevel_index.trectext'
    with open(write_file, 'wb') as f:
        for page in read_data.iter_pages(open(read_file, 'rb')):
            for part in page.skeleton:
                if isinstance(part, read_data.Para):
                    page_text = part.get_text()
                    headline = page.page_name
                    write_to_file(page_text, part.paragraph.para_id, headline, f)
                elif isinstance(part, read_data.Section):
                    headline = str(page.page_name) + '/' + str(part.heading)
                    toplevel_iter_sections(part, headline, f)


build_article()
build_hierarchical()
build_toplevel()
