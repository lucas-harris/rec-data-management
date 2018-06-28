"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import time
import datetime
from models import *

# class Parser():
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
    whole_sheet = result.get('values', [])
    start_cell = 3
    end_cell = 19
    row = 1
    while row < len(whole_sheet):
        current_time = whole_sheet[row-1][0]
        if current_time == '6:30 AM':
            start_cell = row
            end_cell = row + 16
            RANGE_NAME = sheet + '!A' + str(start_cell) + ':AD' + str(end_cell)
            result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
            values = result.get('values', [])
            render_week(values, start_date)
            # print(values)
            row+=16
            time.sleep(1)
        else:
            row += 1


def render_week(week, start_date):
    data_dict = {}
    # for hour in week:
        # time = time_convert_dict[hour[0]]
        # day_dict = {}
        # day_dict['monday'] = convert_day_to_gender_dictionary(hour[1:5])
        # day_dict['tuesday'] = convert_day_to_gender_dictionary(hour[5:9])
        # day_dict['wednesday'] = convert_day_to_gender_dictionary(hour[9:13])
        # day_dict['thursday'] = convert_day_to_gender_dictionary(hour[13:17])
        # day_dict['friday'] = convert_day_to_gender_dictionary(hour[17:21])
        # day_dict['saturday'] = convert_day_to_gender_dictionary(hour[21:25])
        # day_dict['sunday'] = convert_day_to_gender_dictionary(hour[25:29])

    hour = week[0]    
    convert_row_to_dictionary(hour, start_date, 'yes')
        
def convert_row_to_dictionary(row, date, data_dict):
    time_convert_dict = {'6:30 AM':'0630', '7:30 AM':'0730', '8:30 AM':'0830', '9:30 AM':'0930', '10:30 AM':'1030', '11:30 AM':'1130', '12:30 PM':'1230', '1:30 PM':'1330', '2:30 PM':'1430', '3:30 PM':'1530', '4:30 PM':'1630', '5:30 PM':'1730', '6:30 PM':'1830', '7:30 PM':'1930', '8:30 PM':'2030', '9:30 PM':'2130', '10:30 PM':'2230'}
    return_data_dictionary = {}
    time = time_convert_dict[row[0]]
    current_index = 1
    hour_dict = {}
    for day in range(0,7):
        m_fc = {'gender':'m', 'facility':'rec', 'time':time, 'area':'fc', 'date':date + datetime.timedelta(days=day), 'value':check_string(row[current_index])}
        current_index += 1
        f_fc = {'gender':'f', 'facility':'rec', 'time':time, 'area':'fc', 'date':date + datetime.timedelta(days=day), 'value':check_string(row[current_index])}
        current_index += 1
        m_gf = {'gender':'m', 'facility':'rec', 'time':time, 'area':'gf', 'date':date + datetime.timedelta(days=day), 'value':check_string(row[current_index])}
        current_index += 1
        f_gf = {'gender':'f', 'facility':'rec', 'time':time, 'area':'gf', 'date':date + datetime.timedelta(days=day), 'value':check_string(row[current_index])}
        current_index += 1
        day_dict = {'m_fc': m_fc, 'f_fc':f_fc, 'm_gf':m_gf, 'f_gf':f_gf}
        hour_dict[date + datetime.timedelta(days=day)] = day_dict
    for day in hour_dict.values():
        for data in day.values():
            key = str(data['date'])[0:10] + ' ' + data['facility'] + ' ' + data['area'] + ' ' + data['time'] + ' ' + data['gender']
            data = Data(key=key, value=data['value'], facility=data['facility'], area=data['area'], time=data['time'], gender=data['gender'], date_id=data['date'])


def check_string(string):
    try: 
        return int(string)
    except ValueError:
        return None

parse_sheet('Rec Patron Counts', datetime.datetime(2017, 8, 27))
