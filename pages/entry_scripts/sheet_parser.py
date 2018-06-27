"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import time
from datetime import date

def parse_sheet(sheet, start_date):
    column_dict = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P', 16:'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y', 25:'Z', 26:'AA', 27:'AB', 28:'AC'}
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    SPREADSHEET_ID = '16W_a0IBG_xSflQhOBSOKvIHb7S5kp25lCinJuug5w5w'
    RANGE_NAME = sheet
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    for row in range(1,len(values)):
        
        RANGE_NAME = sheet + '!A' + str(row)
        result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get('values', [])
        current_time = values
        if current_time == '6:30 AM':
            print('yes')
            for column in range(1, 30):
                RANGE_NAME = sheet + '!' + column_dict[column] + str(row)
                result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
                values = result.get('values', [])
                print(values)
                time.sleep(1)
        # if not values:
        #     print('hello')
        # else:
        #     print(values)
        # time.sleep(1)


parse_sheet('Rec Patron Counts', date(2017, 8, 27))