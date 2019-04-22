from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import time
import datetime
import psycopg2
import gspread
from oauth2client.service_account import ServiceAccountCredentials

conn = psycopg2.connect(user="postgres", password="password", host='35.239.79.43', dbname="recdb")
# conn.rollback()
sql = conn.cursor()

'''Reads the patron count spread sheet and sends a week's worth of counts to the render_week methods'''
def parse_sheet(sheet):
    column_dict = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P', 16:'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y', 25:'Z', 26:'AA', 27:'AB', 28:'AC'}
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('rec-data-7e58469dd779.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open("Patron Counts - Fall 201  (All Facilities)").worksheet(sheet)
    whole_sheet = wks.get_all_values()
    RANGE_NAME = sheet
    start_cell = 3
    row = 3
    # key_arr = []
    # facility_arr = []
    # area_arr = []
    # time_arr = []
    # gender_arr = []
    # value_arr = []
    # date_arr = []
    if sheet == 'Rec Patron Counts':
        current_date = datetime.datetime(2017, 8, 28)
        end_cell = 19
        insert_command = "INSERT INTO data VALUES "#(key, facility, area, time, gender, value, date) VALUES '
        # update_command = " "
        while row < len(whole_sheet):
            current_time = whole_sheet[row-1][0]
            if current_time == '6:30 AM':
                start_cell = row
                end_cell = row + 16
                # print(whole_sheet[start_cell-1:end_cell])
                commands = render_week_rec(whole_sheet[start_cell-1:end_cell], current_date)
                insert_command += commands
                # key_arr += (commands['key'])
                # facility_arr += (commands['facility'])
                # area_arr += (commands['area'])
                # time_arr += (commands['time'])
                # gender_arr += (commands['gender'])
                # value_arr += (commands['value'])
                # date_arr += (commands['date'])
                row+=1
                current_date = current_date + datetime.timedelta(days=7)
            else:
                row += 1
        insert_command = insert_command[0:len(insert_command)-1] + " ON CONFLICT (key) DO NOTHING;"
        sql.execute(insert_command)
        conn.commit()
    elif sheet == 'Clawson':
        # current_date = datetime.datetime(2017, 11, 6)
        # end_cell = 21
        # while row < len(whole_sheet):
        #     current_time = whole_sheet[row-1][0]
        #     if current_time == '2:30':
        #         start_cell = row
        #         end_cell = row + 18
        #         row+=16
        #         current_date = current_date + datetime.timedelta(days=7)
        #     else:
        #         row += 1
        current_date = datetime.datetime(2017, 11, 6)
        end_cell = 21
        insert_command = "INSERT INTO data VALUES "#(key, facility, area, time, gender, value, date) VALUES '
        # update_command = " "
        while row < len(whole_sheet):
            current_time = whole_sheet[row-1][0]
            if current_time == '2:30':
                start_cell = row
                end_cell = row + 18
                # print(whole_sheet[start_cell-1:end_cell])
                commands = render_week_clawson(whole_sheet[start_cell-1:end_cell], current_date)
                insert_command += commands
                # key_arr += (commands['key'])
                # facility_arr += (commands['facility'])
                # area_arr += (commands['area'])
                # time_arr += (commands['time'])
                # gender_arr += (commands['gender'])
                # value_arr += (commands['value'])
                # date_arr += (commands['date'])
                row+=1
                current_date = current_date + datetime.timedelta(days=7)
            else:
                row += 1
        insert_command = insert_command[0:len(insert_command)-1] + " ON CONFLICT (key) DO NOTHING;"
        # sql.execute(insert_command)
        # conn.commit()
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
                row+=18
                current_date = current_date + datetime.timedelta(days=7)
            else:
                row += 1

'''Adds a week of counts from the "Rec Patron Count" sheet to the database'''
def render_week_rec(week, date):
    full_command = ""
    key_arr = []
    facility_arr = []
    area_arr = []
    time_arr = []
    gender_arr = []
    value_arr = []
    date_arr = []
    for hour in week:
        # conn.rollback()
        time_convert_dict = {'6:30 AM':'06:30', '7:30 AM':'07:30', '8:30 AM':'08:30', '9:30 AM':'09:30', '10:30 AM':'10:30', '11:30 AM':'11:30', '12:30 PM':'12:30', '1:30 PM':'13:30', '2:30 PM':'14:30', '3:30 PM':'15:30', '4:30 PM':'16:30', '5:30 PM':'17:30', '6:30 PM':'18:30', '7:30 PM':'19:30', '8:30 PM':'20:30', '9:30 PM':'21:30', '10:30 PM':'22:30'}
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
                if not data == None and not data['value'] == None:
                    key = str(data['date'])[0:10] + ' ' + data['facility'] + ' ' + data['area'] + ' ' + data['time'] + ' ' + data['gender']
                    full_command += "('" + key + "', '" + data['facility'] + "', '" + data['area'] + "', '" + data['time'] + "', '" + data['gender'] + "', '" + str(data['value']) + "', '" + str(data['date'])[0:10] + "')," #ON CONFLICT (key) DO UPDATE SET value=" + str(data['value'])+ ";"
                    key_arr.append(key)
                    facility_arr.append(data['facility'])
                    area_arr.append(data['area'])
                    time_arr.append(data['time'])
                    gender_arr.append(data['gender'])
                    value_arr.append(str(data['value']))
                    date_arr.append(str(data['date'])[0:10])
    return full_command
    # return {"full_command":full_command, "key":key_arr, "facility":facility_arr, "area":area_arr, "time":time_arr, "gender":gender_arr, "value":value_arr, "date":date_arr} 
                    # print(command)
                    # sql.execute(command)
                    # try:
                    #     conn.commit()
                    # except BaseException:
                    #     conn.rollback()


'''Adds a week of counts from the "Rec Patron Count" sheet to the database'''
def render_week_clawson(week, date):
    time_convert_dict = {'2:30':'14:30', '3:30':'15:30', '4:30':'16:30', '5:30':'17:30', '6:30':'18:30', '7:30':'19:30', '8:30':'20:30', '9:30':'21:30'}
    hour_dict = {}
    full_command = ""
    for hour in week[0:8]:
        full_command = ""
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
                if not data == None and not data['value'] == None:
                    key = str(data['date'])[0:10] + ' ' + data['facility'] + ' ' + data['area'] + ' ' + data['time'] + ' ' + data['gender']
                    full_command += "('" + key + "', '" + data['facility'] + "', '" + data['area'] + "', '" + data['time'] + "', '" + data['gender'] + "', '" + str(data['value']) + "', '" + str(data['date'])[0:10] + "')," #ON CONFLICT (key) DO UPDATE SET value=" + str(data['value'])+ ";"
                    # command = "INSERT INTO data VALUES ('" + key + "', '" + data['facility'] + "', '" + data['area'] + "', '" + data['time'] + "', '" + data['gender'] + "', '" + str(data['value']) + "', '" + str(data['date'])[0:10] + "') ON CONFLICT (key) DO NOTHING;"
                    print(full_command)
                    # sql.execute(command)
    date = date + datetime.timedelta(days=4)
    for hour in week[11:19]:
        full_command = ""
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
                if not data == None and not data['value'] == None:
                    key = str(data['date'])[0:10] + ' ' + data['facility'] + ' ' + data['area'] + ' ' + data['time'] + ' ' + data['gender']
                    full_command += "('" + key + "', '" + data['facility'] + "', '" + data['area'] + "', '" + data['time'] + "', '" + data['gender'] + "', '" + str(data['value']) + "', '" + str(data['date'])[0:10] + "')," #ON CONFLICT (key) DO UPDATE SET value=" + str(data['value'])+ ";"
                    print(full_command)


'''Adds a week of counts from the "North Quad" sheet to the database'''            
def render_week_nq(week, date):
    time_convert_dict = {'2:30':'14:30', '3:30':'15:30', '4:30':'16:30', '5:30':'17:30', '6:30':'18:30', '7:30':'19:30', '8:30':'20:30', '9:30':'21:30'}
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
                if not data == None and not data['value'] == None:
                    key = str(data['date'])[0:10] + ' ' + data['facility'] + ' ' + data['area'] + ' ' + data['time'] + ' ' + data['gender']
                    command = "INSERT INTO data VALUES ('" + key + "', '" + data['facility'] + "', '" + data['area'] + "', '" + data['time'] + "', '" + data['gender'] + "', '" + str(data['value']) + "', '" + str(data['date'])[0:10] + "') ON CONFLICT (key) DO NOTHING;"
                    sql.execute(command)
                    try:
                        conn.commit()
                    except BaseException:
                        conn.rollback()
                    # print(command)
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
                if not data == None and not data['value'] == None:
                    key = str(data['date'])[0:10] + ' ' + data['facility'] + ' ' + data['area'] + ' ' + data['time'] + ' ' + data['gender']
                    command = "INSERT INTO data VALUES ('" + key + "', '" + data['facility'] + "', '" + data['area'] + "', '" + data['time'] + "', '" + data['gender'] + "', '" + str(data['value']) + "', '" + str(data['date'])[0:10] + "') ON CONFLICT (key) DO NOTHING;"
                    sql.execute(command)
                    try:
                        conn.commit()
                    except BaseException:
                        conn.rollback()
                    # print(command) 

'''Searches for a date on the selected sheet and adds that week of counts to the database'''
def update_week(sheet, date):
    loop_flag = True
    date = datetime.datetime.strptime(date.strftime('%Y-%m-%d'), "%Y-%m-%d")
    sheet_info = update_week_advancer(sheet, date)
    date_incrementer = sheet_info['first week']
    column_dict = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P', 16:'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y', 25:'Z', 26:'AA', 27:'AB', 28:'AC'}
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('rec-data-7e58469dd779.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open("Patron Counts - Fall 201  (All Facilities)").worksheet(sheet)
    whole_sheet = wks.get_all_values()
    row = sheet_info['start cell']
    start_cell = row
    end_cell = row + sheet_info['increment']
    while loop_flag and row<len(whole_sheet):
        current_time = whole_sheet[row-1][0]
        if current_time == sheet_info['time']:
            print(date_incrementer)
            if date >= date_incrementer and date <= date_incrementer + datetime.timedelta(days=6):
                loop_flag = False
                start_cell = row
                end_cell = row + sheet_info['increment']
                values = whole_sheet[start_cell-1:end_cell]
                # print(values)
                if sheet=='Rec Patron Counts':
                    render_week_rec(values, date_incrementer)
                elif sheet=='North Quad':
                    render_week_nq(values, date_incrementer)
                elif sheet=='Clawson':
                    render_week_clawson(values, date_incrementer)
            else:
                date_incrementer = date_incrementer + datetime.timedelta(days=7)
                row += sheet_info['increment']
        else:
            row += 1

'''Returns information needed to parse the sheet for the update_week method'''
def update_week_advancer(sheet, date):
    if sheet == 'Rec Patron Counts':
        return {'first week':datetime.datetime(2017, 8, 28), 'start cell': 3, 'end cell': 19, 'increment':16, 'range_end':'AD', 'time':'6:30 AM'}
    elif sheet == 'Clawson':
        if date < datetime.datetime(2019, 1, 28):
            return {'first week':datetime.datetime(2017, 11, 6),'start cell': 3, 'end cell': 21, 'increment':18, 'range_end':'S', 'time':'2:30'}
        else:
            return {'first week':datetime.datetime(2019, 1, 28),'start cell': 1180, 'end cell': 1198, 'increment':18, 'range_end':'S', 'time':'2:30'}
    elif sheet == 'North Quad':
        if date < datetime.datetime(2018, 8, 27):
            return {'first week':datetime.datetime(2017, 10, 30),'start cell': 220, 'end cell': 238, 'increment':18, 'range_end':'S', 'time':'2:30'}
        elif date < datetime.datetime(2019, 1, 28):
            return {'first week':datetime.datetime(2018, 8, 27),'start cell': 1516, 'end cell': 1534, 'increment':18, 'range_end':'S', 'time':'2:30'}
        else:
            return {'first week':datetime.datetime(2019, 1, 28),'start cell': 1950, 'end cell': 1968, 'increment':18, 'range_end':'S', 'time':'2:30'}

'''Parses all three patron count sheets'''
def parse_all():
    parse_sheet('Rec Patron Counts')
    parse_sheet('Clawson')
    parse_sheet('North Quad')

'''Updates one week of all three patrons count sheets'''
def update_all(date):
    update_week('Rec Patron Counts', date)
    update_week('Clawson', date)
    update_week('North Quad', date)

'''Checks that a cell contains a number and not text'''
def check_string(string):
    try: 
        return int(string)
    except ValueError:
        return None

def bulk_insert(temp_command, full_command):
    # sql.execute("select value from data where key='2019-02-01 rec gf 16:30 f';")
    # print(sql.fetchall())
    sql.execute("create table temp (key varchar(40) primary key, facility varchar(20), area varchar(20), time varchar(10), gender varchar (2), value integer, date date);")
    # sql.execute(temp_command)
    # sql.execute("insert into data (key, facility, area, time, gender, value, date) select key, facility, area, time, gender, value, date from temp where key='2019-04-01 rec gf 16:30 f' on conflict (key) do update set key = excluded.key, facility = excluded.facility, area = excluded.area, time = excluded.time,  gender = excluded.gender, value = excluded.value, date = excluded.date;")
    # sql.execute("DROP TABLE temp;")
    sql.execute(temp_command)
    sql.execute(full_command)


'''Reads the data in a cell and estimates it if there is none'''
def gather_data_from_cell(hour, date, day, facility, area, time, gender, current_index):
    estimated = False
    value = 0
    if not hour[current_index]:
        # if len() == 0:
        #     value = 0
        # else:
        return None
    else:
        value = check_string(hour[current_index])
    return {'gender':gender, 'facility':facility, 'time':time, 'area':area, 'date':date + datetime.timedelta(days=day), 'value':value, 'estimated':estimated}

'''Reads the queryset used to estimate an empty cell and finds the average of it'''
def make_average(queryset):
    total = 0
    length = 0
    for number in queryset:
        if number.value:
            total += number.value
    return total/len(queryset)

def replace_comma_with_semicolon(command):
    command = command[0:len(command)-1]
    return command + ' on conflict do nothing;'