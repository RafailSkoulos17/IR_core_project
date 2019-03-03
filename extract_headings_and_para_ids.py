from trec_car import read_data


def write_to_file(para_id, headline, f):
    f.write(bytes(str(headline), 'utf8') + b"    " + bytes(str(para_id), 'utf8') + b"\n")


def hierarchical_iter_sections(section, headline, f):
    headline += '/' + section.heading
    for part in section.children:
        if isinstance(part, read_data.Para):
            write_to_file(part.paragraph.para_id, headline, f)
        elif isinstance(part, read_data.Section):
            hierarchical_iter_sections(part, headline, f)


def build_hierarchical():
    # read_file = r'benchmarkY1\benchmarkY1-train\train.pages.cbor'
    read_file = r'test200-train\train.pages.cbor'
    write_file = 'rankLib/hierarchical.txt'
    with open(write_file, 'wb') as f:
        for page in read_data.iter_pages(open(read_file, 'rb')):
            for part in page.skeleton:
                if isinstance(part, read_data.Para):
                    headline = page.page_name
                    write_to_file(part.paragraph.para_id, headline, f)
                elif isinstance(part, read_data.Section):
                    headline = page.page_name
                    hierarchical_iter_sections(part, headline, f)



def toplevel_iter_sections(section, headline, f):
    for part in section.children:
        if isinstance(part, read_data.Para):
            write_to_file(part.paragraph.para_id, headline, f)
        elif isinstance(part, read_data.Section):
            article_iter_sections(part, headline, f)


def article_iter_sections(section, headline, f):
    for part in section.children:
        if isinstance(part, read_data.Para):
            write_to_file(part.paragraph.para_id, headline, f)
        elif isinstance(part, read_data.Section):
            article_iter_sections(part, headline, f)


def build_article():
    # read_file = r'benchmarkY1\benchmarkY1-train\train.pages.cbor'
    read_file = r'test200-train\train.pages.cbor'
    write_file = 'rankLib/article.txt'
    with open(write_file, 'wb') as f:
        for page in read_data.iter_pages(open(read_file, 'rb')):
            headline = page.page_name
            for part in page.skeleton:
                if isinstance(part, read_data.Para):
                    write_to_file(part.paragraph.para_id, headline, f)
                elif isinstance(part, read_data.Section):
                    article_iter_sections(part, headline, f)


def build_toplevel():
    # read_file = r'benchmarkY1\benchmarkY1-train\train.pages.cbor'
    read_file = r'test200-train\train.pages.cbor'
    write_file = r'rankLib\toplevel.txt'
    with open(write_file, 'wb') as f:
        for page in read_data.iter_pages(open(read_file, 'rb')):
            for part in page.skeleton:
                if isinstance(part, read_data.Para):
                    headline = page.page_name
                    write_to_file(part.paragraph.para_id, headline, f)
                elif isinstance(part, read_data.Section):
                    headline = str(page.page_name) + '/' + str(part.heading)
                    toplevel_iter_sections(part, headline, f)


build_hierarchical()
build_article()
build_toplevel()
