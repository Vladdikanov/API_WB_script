import io
import time
import os
import os.path
from openpyxl import load_workbook
import shutil
from pprint import pprint
import base64
from zipfile import ZipFile
import requests
from GS import add_document, create_new_table
from config import sheet_id

def get_headers(api):
    token = api

    headers = {
        "Authorization": token,
        "Content type": "application/json"

    }
    return headers

def get_documents(header, serviceName: str = None) -> list:
    while True:
        params = {
            "category": "weekly-implementation-report"
        }
        if serviceName != None and type(serviceName) == str:
            params["serviceName"] = serviceName
        res = requests.get("https://documents-api.wildberries.ru/api/v1/documents/list", headers=header, params=params)
        if res.status_code != 200:
            error = res.json()
            title = error.get("title")
            detail = error.get("detail")
            print(f"{title}\n{detail}")
            time.sleep(10)
            continue
        break
    data = res.json()
    all_documents = data.get('data', {}).get('documents', {})
    format = 'xlsx'
    main_docs = []
    for doc in all_documents:
        category = doc.get('category')
        name = doc.get('name')
        extensions = doc.get('extensions')
        serviceName = doc.get('serviceName')
        if format in extensions:
            main_docs.append(
                {"name": name,
                 'serviceName': serviceName}
            )
    return main_docs

def download_document(header, title_doc_to_download: str) -> str:

    serviceName = title_doc_to_download
    if os.path.exists(f'{serviceName}') == False:
        os.mkdir(f'{serviceName}')
    else:
        shutil.rmtree(f'{serviceName}')

    while True:
        params = {
            "serviceName": serviceName,
            "extension": "xlsx"
        }
        res = requests.get("https://documents-api.wildberries.ru/api/v1/documents/download", headers=header, params=params)
        if res.status_code != 200:
            error = res.json()
            title = error.get("title")
            detail = error.get("detail")
            print(f"{title}\n{detail}")
            time.sleep(10)
            continue
        break
    data = res.json()
    pprint(data)
    document = data.get('data', {}).get('document')

    binary = base64.b64decode(document)
    zip_buffer = io.BytesIO(binary)


    with ZipFile(zip_buffer) as zip_file:
        zip_file.extractall(f'{serviceName}')
    print("Файл распакован")
    return serviceName


# create_new_table(name_dir_file, sheet_id)
# add_document(cleaned_data, name_dir_file, sheet_id)