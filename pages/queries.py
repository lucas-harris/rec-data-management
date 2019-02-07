import calendar
from collections import OrderedDict
from functools import cmp_to_key
from django import forms
from .models import *
from datetime import *
import psycopg2
import json

conn = psycopg2.connect(user="postgres", password="password", host='35.239.79.43', dbname="recdb")
sql = conn.cursor()
# cur.execute("SELECT * FROM data where facility='rec' and area='gf' and gender='m' and value=10")

month_dict = {'1':'January', '2':'February', '3':'March', '4':'April', '5':'May', '6':'June', '7':'July', '8':'August', '9':'September', '10':'October', '11':'November', '12':'December'}
time_dict = {'06:30': '6:30 AM', '07:30':'7:30 AM', '08:30':'8:30 AM' ,'09:30':'9:30 AM' ,'10:30':'10:30 AM' ,'11:30':'11:30 AM' ,'12:30':'12:30 PM' ,'13:30':'1:30 PM' ,'14:30':'2:30 PM' ,'15:30':'3:30 PM' ,'16:30':'4:30 PM' ,'17:30':'5:30 PM' ,
'18:30':'6:30 PM', '19:30':'7:30 PM', '20:30':'8:30 PM', '21:30':'9:30 PM', '22:30':'10:30 PM'}

class Query:

    #Return Methods
    """Returns a list of all keys from the dictionary containing the sorted results"""
    def return_keys(self, dictionary):
        ret_list = []
        for x in dictionary:
            ret_list.append(x)
        return ret_list

    """Returns a list of all values from the dictionary containing the sorted results"""
    def return_values(self, dictionary):
        ret_list = []
        for x in dictionary:
            ret_list.append(dictionary[x])
        return ret_list

    #Sort Results
    """Sorts a dictionary based on the increment units selected in Dataset form"""
    def sort_results(self, graph):
        dictionary = self.group_queries(graph)
        return_dictionary = OrderedDict()
        inc = graph.unit
        if inc=='day':
            for key in sorted(dictionary, key=cmp_to_key(self.compare_day)):
                return_dictionary[key] = dictionary[key]
            return_dictionary = self.eliminate_duplicates_day(return_dictionary)
        elif inc=='hour':
            for key in sorted(dictionary, key=cmp_to_key(self.compare_hour)):
                return_dictionary[key] = dictionary[key]
            return_dictionary = self.eliminate_duplicates_hour(return_dictionary)
        elif inc=='week':
            for key in sorted(dictionary, key=cmp_to_key(self.compare_week)):
                return_dictionary[key] = dictionary[key]
            return_dictionary = self.eliminate_duplicates_week(return_dictionary)
        elif inc=='month':
            for key in sorted(dictionary, key=cmp_to_key(self.compare_month)):
                return_dictionary[key] = dictionary[key]
            return_dictionary = self.eliminate_duplicates_month(return_dictionary)
        elif inc=='year':
            for key in sorted(dictionary):
                return_dictionary[key] = dictionary[key]
        elif inc=='all':
            return_dictionary = dictionary
        return return_dictionary

    """Shortens label by removing date if all data points took place on the same date"""
    def eliminate_duplicates_hour(self, dictionary):
        year_dictionary = dict()
        return_dictionary = OrderedDict()
        for key in dictionary:
            year_dictionary[key.split(',')[1]] = True
        if len(year_dictionary) == 1:
            for key in dictionary:
                return_dictionary[key.split(',')[0]] = dictionary[key]
            return return_dictionary
        else:
            return dictionary

    """Shortens label by removing year if all data points took place in the same year"""
    def eliminate_duplicates_day(self, dictionary):
        year_dictionary = dict()
        return_dictionary = OrderedDict()
        for key in dictionary:
            year_dictionary[key.split('/')[2]] = True
        if len(year_dictionary) == 1:
            for key in dictionary:
                date_string = calendar.month_name[int(key[0:2])] + ' ' + key[3:5]
                return_dictionary[date_string] = dictionary[key]
            return return_dictionary
        else:
            return dictionary

    """Shortens label by removing year if all data points took place in the same year"""
    def eliminate_duplicates_month(self, dictionary):
        year_dictionary = dict()
        return_dictionary = OrderedDict()
        for key in dictionary:
            year_dictionary[key.split(' ')[1]] = True
        if len(year_dictionary) == 1:
            for key in dictionary:
                return_dictionary[key.split(' ')[0]] = dictionary[key]
            return return_dictionary
        else:
            return dictionary

    """Shortens label by removing year if all data points took place in the same year"""
    def eliminate_duplicates_week(self, dictionary):
        year_dictionary = dict()
        return_dictionary = OrderedDict()
        for key in dictionary:
            year_dictionary[key[8:]] = True
        if len(year_dictionary) == 1:
            for key in dictionary:
                return_dictionary[key[0:7]] = dictionary[key]
            return return_dictionary
        else:
            return dictionary

    """Sorts a dictionary by the month"""
    def compare_month(self, month1, month2):
        calendar = {'January':0, 'February':1, 'March':2, 'April':3, 'May':4, 'June':5, 'July':6, 'August':7, 'September':8, 'October':9, 'November':10, 'December':11}
        split_month1 = month1.split(' ')
        split_month2 = month2.split(' ')
        if split_month1[1] <= split_month2[1]:
            if calendar[split_month1[0]] <= calendar[split_month2[0]]:
                    return -1
            else:
                return 1
        else:
            return 1

    """Sorts a dictionary by the week"""
    def compare_week(self, week1, week2):
        if week1[9:13] <= week2[9:13]: #Year
            if week1[5:7] < week2[5:7]: #Week
                return -1
            else:
                return 1
        else:
            return 1

    """Sorts a dictionary by the day"""
    def compare_day(self, day1, day2):
        if day1[6:10] <= day2[6:10]: #Year
            if day1[0:2] <= day2[0:2]: #Month
                if day1[3:5] < day2[3:5]: #Day
                    return -1
                else:
                    return 1
            else:
                return 1
        else:
            return 1

    """Sorts a dictionary by the hour"""
    def compare_hour(self, hour1, hour2):
        day_check = False 
        if hour1[13:17] <= hour2[13:17]: #Year
            if hour1[7:9] <= hour2[7:9]: #Month
                if hour1[10:12] < hour2[10:12]: #Day
                    return -1
                elif hour1[10:12] == hour2[10:12]:
                    if hour1[0:2] < hour2[0:2]:
                        return -1
                    else:
                        return 1
                else:
                    return 1
            else:
                return 1
        else:
            return 1

    #Increment Grouping
    """Returns a dictionary containing the values of the Data selected in the Dataset form"""
    """grouped by the increment unit selected in the form"""
    def group_queries(self, graph):
        inc = graph.unit
        if inc=='year':
            return self.group_by_year(self.query_every_day(graph))
        elif inc=='month':
            return self.group_by_month(self.query_every_day(graph))
        elif inc=='week':
            return self.group_by_week(self.query_every_day(graph))
        elif inc=='day':
            return self.group_by_day(self.query_every_day(graph))
        elif inc=='hour':
            return self.group_by_hour(self.query_every_day(graph))
        elif inc=='all':
            return self.group_by_all(self.query_every_day(graph))

    """Returns a dictionary with one value that is equal to the sum of all values selected"""
    def group_by_all(self, dictionary):
        value = 0
        for key in dictionary:
            for x in dictionary[key]:
                value += x.value
        return {'all':value}

    """Returns a dictionary with values grouped by the year they took place in"""
    def group_by_year(self, dictionary):
        year_dict = OrderedDict()
        for key in dictionary:
            for x in dictionary[key]:
                if self.make_year_key(x) in year_dict:
                    value = year_dict[self.make_year_key(x)] + x.value
                else:
                    year_dict[self.make_year_key(x)] = 0
                    value = x.value
                year_dict[self.make_year_key(x)] =  value
        return year_dict

    """Returns a string that represents a year group"""
    def make_year_key(self, data):
        return str(data.date.year)

    """Returns a dictionary with values grouped by the month they took place in"""
    def group_by_month(self, dictionary):
        month_dict = OrderedDict()
        for key in dictionary:
            for data in dictionary[key]:
                if self.make_month_key(data) in month_dict:
                    value = month_dict[self.make_month_key(data)] + data.value
                else:
                    month_dict[self.make_month_key(data)] = 0
                    value = data.value
                month_dict[self.make_month_key(data)] =  value
        return month_dict

    #Year included if more than one year is represented in the group
    """Returns a string that represents a month group with year included"""
    def make_month_key(self, data):
        return calendar.month_name[int(data.date.month)] + ' ' + str(data.date.year)

    """Returns a dictionary with values grouped by the week they took place in"""
    def group_by_week(self, dictionary):
        week_dict = OrderedDict()
        for key in dictionary:
            for x in dictionary[key]:
                if self.make_week_key(x) in week_dict:
                    value = week_dict[self.make_week_key(x)] + x.value
                else:
                    week_dict[self.make_week_key(x)] = 0
                    value = x.value
                week_dict[self.make_week_key(x)] =  value
        return week_dict

    """Returns a string that represents a week group"""
    def make_week_key(self, data):
        return 'Week ' + data.date.week + ', ' + str(data.date.year)

    """Returns a dictionary with values grouped by the day they took place in"""
    def group_by_day(self, dictionary):
        day_dict = OrderedDict()
        for key in dictionary:
            for x in dictionary[key]:
                if self.make_day_key(x) in day_dict:
                    value = day_dict[self.make_day_key(x)] + x.value
                else:
                    day_dict[self.make_day_key(x)] = 0
                    value = x.value
                day_dict[self.make_day_key(x)] =  value
        return day_dict

    """Returns a string that represents a day group"""
    def make_day_key(self, data):
        month = ''
        day = ''
        if int(data.date.month)<10:
            month = '0' + data.date.month
        else:
            month = data.date.month
        if int(data.date.day_of_month)<10:
            day = '0' + data.date.day_of_month
        else:
            day = data.date.day_of_month

        return month + '/' + day + '/' + str(data.date.year)

    """Returns a dictionary with values grouped by the hour they took place in"""
    def group_by_hour(self, dictionary):
        hour_dict = OrderedDict()
        for key in dictionary:
            for x in dictionary[key]:
                if self.make_hour_key(x) in hour_dict:
                    value = hour_dict[self.make_hour_key(x)] + x.value
                else:
                    hour_dict[self.make_hour_key(x)] = 0
                    value = x.value
                hour_dict[self.make_hour_key(x)] = value
        return hour_dict

    """Returns a string that represents a hour group"""
    def make_hour_key(self, data):      
        month = ''
        day = ''
        if int(data.date.month)<10:
            month = '0' + data.date.month
        else:
            month = data.date.month
        if int(data.date.day_of_month)<10:
            day = '0' + data.date.day_of_month
        else:
            day = data.date.day_of_month
        hour = data.time[0:2]
        minute = data.time[2:5]
        return hour + ':' + minute + ', ' + month + '/' + day + '/' + str(data.date.year)

    def run(graph):
        queries = Query.query_all(graph)
        labels = Query.make_labels(graph, queries)
        results = {}
        for index, value in enumerate(queries):
            results[labels[index]] = value[0]
        return results

    def make_labels(graph, queries):
        labels = []
        if graph.cleaned_data['units'] == 'hour':
            for hour in queries:
                date = hour[2]
                labels.append(hour[1] + ", " + date.strftime('%m/%d/%Y'))
        elif graph.cleaned_data['units'] == 'day':
            for day in queries:
                date = day[1]
                labels.append(date.strftime('%m/%d/%Y'))
        elif graph.cleaned_data['units'] == 'week':
            for week in queries:
                labels.append("Week " + week[1] + ", " + week[2])
        elif graph.cleaned_data['units'] == 'month':
            for month in queries:
                labels.append(month_dict[month[1]] + " " + month[2])
        elif graph.cleaned_data['units'] == 'year':
            for year in queries:
                labels.append(year[1] + " " + year[2])
        else:
            labels.append("All")
        return labels

    """Returns a QuerySet that matches all the non-date attributes of Dataset form"""
    def query_all(graph):
        facility = Query.query_facility(graph)
        area = Query.query_area(graph)
        dates = Query.query_dates(graph)
        gender = Query.query_gender(graph)
        time =  Query.query_time(graph)
        year = Query.query_year(graph)
        month = Query.query_month(graph)
        week = Query.query_week(graph)
        day_of_month = Query.query_day_of_month(graph)
        day_of_week = Query.query_day_of_week(graph)
        group_by = Query.group_by(graph)
        units = Query.columns_to_query(graph)
        order_by = Query.order_by(graph)
        query = "SELECT SUM(data.value)" + units + " FROM date, data WHERE date.date=data.date"  + facility + area + dates + gender + time + year + month + week + day_of_month + day_of_week + group_by + order_by + ";"
        # return query
        sql.execute(query)
        return sql.fetchall()

    def columns_to_query(graph):
        if graph.cleaned_data['units'] == 'hour':
            return ", data.time, data.date"
        elif graph.cleaned_data['units'] == 'day':
            return ", data.date"
        elif graph.cleaned_data['units'] == 'week':
            return ", date.week, date.year"
        elif graph.cleaned_data['units'] == 'month':
            return ", date.month, date.year"
        elif graph.cleaned_data['units'] == 'year':
            return ", date.year"
        else:
            return ""

    """Returns a QuerySet that is the period and date queries combined"""
    def group_by(graph):
        if graph.cleaned_data['units'] == 'hour':
            return " GROUP BY data.time, data.date"
        elif graph.cleaned_data['units'] == 'day':
            return " GROUP BY data.date"
        elif graph.cleaned_data['units'] == 'week':
            return " GROUP BY date.week, date.year"
        elif graph.cleaned_data['units'] == 'month':
            return " GROUP BY date.month, date.year"
        elif graph.cleaned_data['units'] == 'year':
            return " GROUP BY date.year"
        else:
            return ""

    def order_by(graph):
        if graph.cleaned_data['units'] == 'hour':
            return " ORDER BY data.time, data.date"
        elif graph.cleaned_data['units'] == 'day':
            return " ORDER BY data.date"
        elif graph.cleaned_data['units'] == 'week':
            return " ORDER BY date.week, date.year"
        elif graph.cleaned_data['units'] == 'month':
            return " ORDER BY date.month, date.year"
        elif graph.cleaned_data['units'] == 'year':
            return " ORDER BY date.year"
        else:
            return ""

    """Returns a QuerySet of all dates between the start and end date in Dataset form"""
    def query_dates(graph):
        start_date = graph.cleaned_data['start_date'] - timedelta(days=1)
        start_date = start_date.strftime('%m/%d/%Y')
        end_date = graph.cleaned_data['end_date'] - timedelta(days=1)
        end_date = end_date.strftime('%m/%d/%Y')
        return " AND (data.date>='" + start_date + "' AND data.date<='" + end_date + "')"

    """Returns a QuerySet of all dates that match the values chosen in Dataset form"""
    def get_date_queries(self, graph):
        month = self.query_month(graph)
        week = self.query_week(graph)
        year = self.query_year(graph)
        dom = self.query_day_of_month(graph)
        dow = self.query_day_of_week(graph)
        ret = Date.objects.all()
        if month == 'all' and week == 'all' and year == 'all' and dom == 'all' and dow == 'all':
            return ret
        if not month == 'all':
            ret = ret & month 
        if not week == 'all':
            ret = ret & week 
        if not year == 'all':
            ret = ret & year
        if not dom == 'all':
            ret = ret & dom
        if not dow == 'all':
            ret = ret & dow
        return ret


    #Date Queries-------------------------
    """Returns a QuerySet of all the years selected in the Dataset form"""
    def query_year(graph):
        return Query.query_form_date_checkbox(graph, 'year')

    """Returns a QuerySet of all the months selected in the Dataset form"""
    def query_month(graph):
        return Query.query_form_date_checkbox(graph, 'month')

    """Returns a QuerySet of all the days of the month selected in the Dataset form"""
    def query_day_of_month(graph):
        return Query.query_form_date_checkbox(graph, 'day_of_month')

    """Returns a QuerySet of all the weeks selected in the Dataset form"""
    def query_week(graph):
        return Query.query_form_date_checkbox(graph, 'week')

    """Returns a QuerySet of all the days of the week selected in the Dataset form"""
    def query_day_of_week(graph):
        return Query.query_form_date_checkbox(graph, 'day_of_week')

    #Data Queries-------------------------
    """Returns a QuerySet of all the facilities selected in the Dataset form"""
    def query_facility(graph):
        return Query.query_form_data_checkbox(graph, 'facility')

    """Returns a QuerySet of all the areas selected in the Dataset form"""
    def query_area(graph):
        return Query.query_form_data_checkbox(graph, 'area')

    """Returns a QuerySet of the gender selected in the Dataset form"""
    def query_gender(graph):
        return Query.query_form_data_radio(graph, 'gender')

    """Returns a QuerySet of all the times selected in the Dataset form"""
    def query_time(graph):
        return Query.query_form_data_checkbox(graph, 'time')

    def query_form_data_checkbox(graph, attribute):
        attributes = graph.cleaned_data[attribute]
        query_string = ' AND ('
        for index, row in enumerate(attributes):
            if index==0:
                if row =='all':
                    return ''
                else: 
                    query_string += "data." + attribute + "='" + row + "'"
            else:
                query_string += " OR data." + attribute + "='" + row + "'"
        query_string += ')'
        return query_string

    def query_form_data_radio(graph, attribute):
        attributes = graph.cleaned_data[attribute]
        query_string = ' AND ('
        if attributes =='all':
            return ''
        else: 
            query_string += "data." + attribute + "='" + attributes + "'"
        query_string += ')'
        return query_string

    def query_form_date_checkbox(graph, attribute):
        attributes = graph.cleaned_data[attribute]
        query_string = ' AND ('
        for index, row in enumerate(attributes):
            if index==0:
                if row =='all':
                    return ''
                else: 
                    query_string += "date." + attribute + "='" + row + "'"
            else:
                query_string += " OR date." + attribute + "='" + row + "'"
        query_string += ')'
        return query_string

    def query_form_date_radio(graph, attribute):
        attributes = graph.cleaned_data[attribute]
        query_string = ' AND ('
        if attributes =='all':
            return ''
        else: 
            query_string += "date." + attribute + "='" + attributes + "'"
        query_string += ')'
        return query_string

    #Replace Characters----------------
    """Replaces characters and splits a attributes to return a list of strings"""
    def replace_characters(self, attributes):
        if type(attributes) is list:
            return attributes
        else:
            attributes = attributes.replace('[','')
            attributes = attributes.replace(']','')
            attributes = attributes.replace("'",'')
            attributes = attributes.replace(",",'')
            attributes = attributes.split()
            return attributes

