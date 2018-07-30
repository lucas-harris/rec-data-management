"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import time
import datetime
from pages.models import Data, Date

def parse_sheet(sheet):
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
    row = 1
   
    if sheet == 'Rec Patron Counts':
        current_date = datetime.datetime(2017, 8, 28)
        end_cell = 19
        while row < len(whole_sheet):
            current_time = whole_sheet[row-1][0]
            if current_time == '6:30 AM':
                start_cell = row
                end_cell = row + 16
                RANGE_NAME = sheet + '!A' + str(start_cell) + ':AD' + str(end_cell)
                result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
                values = result.get('values', [])
                render_week_rec(values, current_date)
                row+=16
                current_date = current_date + datetime.timedelta(days=7)
            else:
                row += 1
    elif sheet == 'Clawson':
        current_date = datetime.datetime(2017, 11, 6)
        end_cell = 21
        while row < len(whole_sheet):
            current_time = whole_sheet[row-1][0]
            if current_time == '2:30':
                start_cell = row
                end_cell = row + 18
                RANGE_NAME = sheet + '!A' + str(start_cell) + ':S' + str(end_cell)
                result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
                values = result.get('values', [])
                render_week_clawson(values, current_date)
                row += 18
                current_date = current_date + datetime.timedelta(days=7)
            else:
                row += 1
    elif sheet == 'North Quad':
        current_date = datetime.datetime(2017, 10, 30)
        start_cell = 220
        end_cell = 238
        row = 220
        while row < len(whole_sheet):
            current_time = whole_sheet[row-1][0]
            if current_time == '2:30':
                start_cell = row
                end_cell = row + 18
                RANGE_NAME = sheet + '!A' + str(start_cell) + ':S' + str(end_cell)
                result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
                values = result.get('values', [])
                render_week_nq(values, current_date)
                row += 18
                current_date = current_date + datetime.timedelta(days=7)
            else:
                row += 1

def render_week_rec(week, date):
    for hour in week:
        time_convert_dict = {'6:30 AM':'0630', '7:30 AM':'0730', '8:30 AM':'0830', '9:30 AM':'0930', '10:30 AM':'1030', '11:30 AM':'1130', '12:30 PM':'1230', '1:30 PM':'1330', '2:30 PM':'1430', '3:30 PM':'1530', '4:30 PM':'1630', '5:30 PM':'1730', '6:30 PM':'1830', '7:30 PM':'1930', '8:30 PM':'2030', '9:30 PM':'2130', '10:30 PM':'2230'}
        time = time_convert_dict[hour[0]]
        current_index = 1
        current_value = 0
        hour_dict = {}
        for day in range(0,7):
            m_fc = gather_data_from_cell(hour, date, day, 'rec', 'fc', time, 'm', current_index)
            current_index += 1
            f_fc = gather_data_from_cell(hour, date, day, 'rec', 'fc', time, 'f', current_index)
            current_index += 1
            m_gf = gather_data_from_cell(hour, date, day, 'rec', 'gf', time, 'm', current_index)
            current_index += 1
            f_gf = gather_data_from_cell(hour, date, day, 'rec', 'gf', time, 'f', current_index)
            current_index += 1
            day_dict = {'m_fc': m_fc, 'f_fc':f_fc, 'm_gf':m_gf, 'f_gf':f_gf}
            hour_dict[date + datetime.timedelta(days=day)] = day_dict
        for day in hour_dict.values():
            for data in day.values():
                if not data['value'] == None:
                    key = str(data['date'])[0:10] + ' ' + data['facility'] + ' ' + data['area'] + ' ' + data['time'] + ' ' + data['gender']
                    data = Data(key=key, value=data['value'], facility=data['facility'], area=data['area'], time=data['time'], gender=data['gender'], date_id=data['date'])
                    data.save()

def render_week_clawson(week, date):
    time_convert_dict = {'2:30':'1430', '3:30':'1530', '4:30':'1630', '5:30':'1730', '6:30':'1830', '7:30':'1930', '8:30':'2030', '9:30':'2130'}
    hour_dict = {}
    for hour in week[0:8]:
        time = time_convert_dict[hour[0]]
        current_index = 1
        for day in range(0,4):
            m_fc = gather_data_from_cell(hour, date, day, 'clawson', 'fc', time, 'm', current_index)
            current_index += 1
            f_fc = gather_data_from_cell(hour, date, day, 'clawson', 'fc', time, 'f', current_index)
            current_index += 1
            m_gf = gather_data_from_cell(hour, date, day, 'clawson', 'gf', time, 'm', current_index)
            current_index += 1
            f_gf = gather_data_from_cell(hour, date, day, 'clawson', 'gf', time, 'f', current_index)
            current_index += 1
            day_dict = {'m_fc': m_fc, 'f_fc':f_fc, 'm_gf':m_gf, 'f_gf':f_gf}
            hour_dict[date + datetime.timedelta(days=day)] = day_dict
        for day in hour_dict.values():
            for data in day.values():
                if not data['value'] == None:
                    key = str(data['date'])[0:10] + ' ' + data['facility'] + ' ' + data['area'] + ' ' + data['time'] + ' ' + data['gender']
                    data = Data(key=key, value=data['value'], facility=data['facility'], area=data['area'], time=data['time'], gender=data['gender'], date_id=data['date'])
                    data.save()
    date = date + datetime.timedelta(days=4)
    for hour in week[11:19]:
        time = time_convert_dict[hour[0]]
        current_index = 1
        for day in range(0,3):
            m_fc = gather_data_from_cell(hour, date, day, 'clawson', 'fc', time, 'm', current_index)
            current_index += 1
            f_fc = gather_data_from_cell(hour, date, day, 'clawson', 'fc', time, 'f', current_index)
            current_index += 1
            m_gf = gather_data_from_cell(hour, date, day, 'clawson', 'gf', time, 'm', current_index)
            current_index += 1
            f_gf = gather_data_from_cell(hour, date, day, 'clawson', 'gf', time, 'f', current_index)
            current_index += 1
            day_dict = {'m_fc': m_fc, 'f_fc':f_fc, 'm_gf':m_gf, 'f_gf':f_gf}
            hour_dict[date + datetime.timedelta(days=day)] = day_dict
        for day in hour_dict.values():
            for data in day.values():
                if not data['value'] == None:
                    key = str(data['date'])[0:10] + ' ' + data['facility'] + ' ' + data['area'] + ' ' + data['time'] + ' ' + data['gender']
                    data = Data(key=key, value=data['value'], facility=data['facility'], area=data['area'], time=data['time'], gender=data['gender'], date_id=data['date'])
                    data.save()
            
def render_week_nq(week, date):
    time_convert_dict = {'2:30':'1430', '3:30':'1530', '4:30':'1630', '5:30':'1730', '6:30':'1830', '7:30':'1930', '8:30':'2030', '9:30':'2130'}
    hour_dict = {}
    for hour in week[0:8]:
        time = time_convert_dict[hour[0]]
        current_index = 1
        for day in range(0,4):
            m_fc = gather_data_from_cell(hour, date, day, 'nq', 'fc', time, 'm', current_index)
            current_index += 1
            f_fc = gather_data_from_cell(hour, date, day, 'nq', 'fc', time, 'f', current_index)
            current_index += 1
            m_gf = gather_data_from_cell(hour, date, day, 'nq', 'gf', time, 'm', current_index)
            current_index += 1
            f_gf = gather_data_from_cell(hour, date, day, 'nq', 'gf', time, 'f', current_index)
            current_index += 1
            day_dict = {'m_fc': m_fc, 'f_fc':f_fc, 'm_gf':m_gf, 'f_gf':f_gf}
            hour_dict[date + datetime.timedelta(days=day)] = day_dict
        for day in hour_dict.values():
            for data in day.values():
                if not data['value'] == None:
                    key = str(data['date'])[0:10] + ' ' + data['facility'] + ' ' + data['area'] + ' ' + data['time'] + ' ' + data['gender']
                    data = Data(key=key, value=data['value'], facility=data['facility'], area=data['area'], time=data['time'], gender=data['gender'], date_id=data['date'])
                    data.save()
    date = date + datetime.timedelta(days=4)
    for hour in week[11:19]:
        time = time_convert_dict[hour[0]]
        current_index = 1
        for day in range(0,3):
            m_fc = gather_data_from_cell(hour, date, day, 'nq', 'fc', time, 'm', current_index)
            current_index += 1
            f_fc = gather_data_from_cell(hour, date, day, 'nq', 'fc', time, 'f', current_index)
            current_index += 1
            m_gf = gather_data_from_cell(hour, date, day, 'nq', 'gf', time, 'm', current_index)
            current_index += 1
            f_gf = gather_data_from_cell(hour, date, day, 'nq', 'gf', time, 'f', current_index)
            current_index += 1
            day_dict = {'m_fc': m_fc, 'f_fc':f_fc, 'm_gf':m_gf, 'f_gf':f_gf}
            hour_dict[date + datetime.timedelta(days=day)] = day_dict
        for day in hour_dict.values():
            for data in day.values():
                if not data['value'] == None:
                    key = str(data['date'])[0:10] + ' ' + data['facility'] + ' ' + data['area'] + ' ' + data['time'] + ' ' + data['gender']
                    data = Data(key=key, value=data['value'], facility=data['facility'], area=data['area'], time=data['time'], gender=data['gender'], date_id=data['date'], estimated=data['estimated'])
                    data.save()

def update_week(sheet, date):
    sheet_info = update_week_advancer(sheet)
    loop_flag = True
    date = datetime.datetime.strptime(date.strftime('%Y-%m-%d'), "%Y-%m-%d")
    date_incrementer = sheet_info['first week']
    start_cell = sheet_info['start cell']
    end_cell = sheet_info['end cell']
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
    row = 3
    while loop_flag and row<len(whole_sheet):
        current_time = whole_sheet[row-1][0]
        if current_time == sheet_info['time']:
            start_cell = row
            end_cell = row + sheet_info['increment']
            row += sheet_info['increment']
            if date >= date_incrementer and date <= date_incrementer + datetime.timedelta(days=6):
                loop_flag = False
                RANGE_NAME = sheet + '!A' + str(start_cell) + ':' + sheet_info['range_end'] + str(end_cell)
                result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
                values = result.get('values', [])
                if sheet=='Rec Patron Counts':
                    render_week_rec(values, date_incrementer)
                elif sheet=='North Quad':
                    render_week_nq(values, date_incrementer)
                elif sheet=='Clawson':
                    render_week_clawson(values, date_incrementer)
            else:
                date_incrementer = date_incrementer + datetime.timedelta(days=7)
        else:
            row += 1

def update_week_advancer(sheet):
    if sheet == 'Rec Patron Counts':
        return {'first week':datetime.datetime(2017, 8, 28), 'start cell': 3, 'end cell': 19, 'increment':16, 'range_end':'AD', 'time':'6:30 AM'}
    elif sheet == 'Clawson':
        return {'first week':datetime.datetime(2017, 11, 6),'start cell': 3, 'end cell': 21, 'increment':18, 'range_end':'S', 'time':'2:30'}
    elif sheet == 'North Quad':
        return {'first week':datetime.datetime(2017, 10, 30),'start cell': 220, 'end cell': 238, 'increment':18, 'range_end':'S', 'time':'2:30'}

def parse_all():
    parse_sheet('Rec Patron Counts')
    parse_sheet('Clawson')
    parse_sheet('North Quad')

def update_all(date):
    update_week('Rec Patron Counts', date)
    update_week('Clawson', date)
    update_week('North Quad', date)

def check_string(string):
    try: 
        return int(string)
    except ValueError:
        return None

def gather_data_from_cell(hour, date, day, facility, area, time, gender, current_index):
    estimated = False
    value = 0
    if not hour[current_index]:
        current_day_query = Date.objects.filter(date = (date + datetime.timedelta(days=day-14)))
        current_day_query = current_day_query | Date.objects.filter(date = (date + datetime.timedelta(days=day-7)))
        current_day_query = current_day_query | Date.objects.filter(date = (date + datetime.timedelta(days=day+7)))
        current_day_query = current_day_query | Date.objects.filter(date = (date + datetime.timedelta(days=day+14)))
        cell_query = Data.objects.filter(date_id__in = current_day_query)
        cell_query = cell_query & Data.objects.filter(time=time)
        current_cell_query = cell_query & Data.objects.filter(facility=facility)
        current_cell_query = current_cell_query & Data.objects.filter(area=area)
        current_cell_query = current_cell_query & Data.objects.filter(gender=gender)
        if len(current_cell_query) == 0:
            value = 0
            estimated = True
        else:
            value = make_average(current_cell_query)
            estimated = True
    else:
        value = check_string(hour[current_index])
    return {'gender':gender, 'facility':facility, 'time':time, 'area':area, 'date':date + datetime.timedelta(days=day), 'value':value, 'estimated':estimated}

def make_average(queryset):
    total = 0
    length = 0
    for number in queryset:
        if number.value:
            total += number.value
    return total/len(queryset)