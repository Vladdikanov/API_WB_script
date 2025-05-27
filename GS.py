
import httplib2
from apiclient import discovery
from config import CREEDS
from oauth2client.service_account import ServiceAccountCredentials


creeds = CREEDS

def add_document(data, sheet_name, sheet_id):
    CREDENTIALS_FILE = creeds
    spreadsheet_id = sheet_id
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/spreadsheets'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = discovery.build("sheets", 'v4', http=httpAuth)

    values = data
    body = {"values": values}
    result = (service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=f'{sheet_name}!A1:U',
            valueInputOption="RAW",
            body=body,
        )
        .execute()
    )


def create_new_table(sheet_name, sheet_id):
    CREDENTIALS_FILE = creeds
    spreadsheet_id = sheet_id
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/spreadsheets'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = discovery.build("sheets", 'v4', http=httpAuth)

    body = {
        "requests": {
            "addSheet": {
                "properties": {
                    "title": f"{sheet_name}",
                }
            }
        }
    }

    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

def get_all_lists(sheet_id):
    CREDENTIALS_FILE = creeds
    spreadsheet_id = sheet_id
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/spreadsheets'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = discovery.build("sheets", 'v4', http=httpAuth)

    sheet_info = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheet_list = list(map(lambda x: x['properties']['title'], sheet_info["sheets"]))

    return sheet_list


