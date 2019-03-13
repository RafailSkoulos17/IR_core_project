from trec_car import read_data


# def write_to_file(text, para_id, f):


#
# def article_iter_sections(section, headline, f,qlist):
#     for part in section.children:
#         if isinstance(part, read_data.Para):
#             para_text = part.get_text()
#             if part.paragraph.para_id not in qlist:
#                 write_to_file(para_text, part.paragraph.para_id, f)
#                 qlist += [part.paragraph.para_id]
#         elif isinstance(part, read_data.Section):
#             article_iter_sections(part, headline, f, qlist)
#
#
# def build_article():
#     # read_file = r'benchmarkY1\benchmarkY1-train\train.pages.cbor'
#     read_file = r'test200-train\train.pages.cbor'
#     write_file = 'index_inputs/index.trectext'
#     qlist = []
#     with open(write_file, 'wb') as f:
#         for page in read_data.iter_pages(open(read_file, 'rb')):
#             headli#     write_file = 'index_inputs/index.trectext'ne = page.page_name
#             for part in page.skeleton:
#                 if isinstance(part, read_data.Para):
#                     page_text = part.get_text()
#                     if part.paragraph.para_id not in qlist:
#                         write_to_file(page_text, part.paragraph.para_id, f)
#                         qlist += [part.paragraph.para_id]
#                 elif isinstance(part, read_data.Section):
#                     article_iter_sections(part, headline, f, qlist)
#
# build_article()


def build_trectext(fin):
    i = 0
    fout = open('index.trectext', 'wb')
    ids = {}
    for para in read_data.iter_paragraphs(open(fin, 'rb')):
        if str(para.para_id) not in ids.keys():
            ids[str(para.para_id)] = ""
            i += 1
            print(str(i))

            fout.write(b'<DOC>\n')
            fout.write(b'<DOCNO> ' + bytes(str(para.para_id), 'utf8') + b' </DOCNO>\n')
            text = (para.get_text()).encode('utf8')
            fout.write(b'<TEXT>\n')
            fout.write(text)
            fout.write(b'\n</TEXT>\n')
            fout.write(b'</DOC>\n\n')
    fout.close()


fin = '../train.v2.0.tar/train/base.train.cbor-paragraphs.cbor'
build_trectext(fin)