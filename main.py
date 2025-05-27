from pprint import pprint
from GS import add_document, create_new_table, get_all_lists
from config import sheet_id
from WB_API import get_headers, get_documents, download_document
from config import api_key
from data_prep import parsing_xlsx_file

serviceName: (str, list) = ['weekly-implementation-report-3478562', 'weekly-implementation-report-3376001']



headers = get_headers(api_key)
documents = get_documents(headers, serviceName)
if type(serviceName) == list and bool(serviceName) == True:
    filter_doc = []
    for i in documents:
        sn = i.get('serviceName')
        if sn in serviceName:
            filter_doc.append(i)
    documents = filter_doc
pprint(documents)
for doc in documents:
    pprint(doc)
    title_doc_to_download = doc.get('serviceName')
    file_to_pars = download_document(headers, title_doc_to_download)
    table_name = file_to_pars
    data_to_gs = parsing_xlsx_file(file_to_pars)
    if table_name in get_all_lists(sheet_id):
        print("Таблица уже имеется")
        continue
    create_new_table(table_name, sheet_id)
    add_document(data_to_gs, table_name, sheet_id)























# serviceName = 'weekly-implementation-report-5174724'


# header = get_headers(api_key)
# documents = get_documents(header)
# list_files_to_pars = download_documents(header, documents)
# parsing_xlsx_files(list_files_to_pars)
