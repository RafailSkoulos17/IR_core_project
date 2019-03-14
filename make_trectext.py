from trec_car import read_data


def write_to_file(text, para_id, f):
    f.write(b'<DOC>\n')
    f.write(b'<DOCNO> ' + bytes(str(para_id), 'utf8') + b' </DOCNO>\n')
    text = (text).encode('utf8')
    f.write(b'<TEXT>\n')
    f.write(text)
    f.write(b'\n</TEXT>\n')
    f.write(b'</DOC>\n')



def iter_sections(section, headline, f, qlist):
    for part in section.children:
        if isinstance(part, read_data.Para):
            para_text = part.get_text()
            if part.paragraph.para_id not in qlist:
                write_to_file(para_text, part.paragraph.para_id, f)
                qlist += [part.paragraph.para_id]
        elif isinstance(part, read_data.Section):
            iter_sections(part, headline, f, qlist)


def build_trectext():
    read_file = r'test200-train\train.pages.cbor'
    write_file = 'index_inputs/index.trectext'
    qlist = []
    with open(write_file, 'wb') as f:
        for page in read_data.iter_pages(open(read_file, 'rb')):
            headline = page.page_name
            for part in page.skeleton:
                if isinstance(part, read_data.Para):
                    page_text = part.get_text()
                    if part.paragraph.para_id not in qlist:
                        write_to_file(page_text, part.paragraph.para_id, f)
                        qlist += [part.paragraph.para_id]
                elif isinstance(part, read_data.Section):
                    iter_sections(part, headline, f, qlist)


build_trectext()
