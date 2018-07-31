import calendar
from collections import OrderedDict
from functools import cmp_to_key
from django import forms
from .models import *
from datetime import *

class Query():
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

#Combination of Queries-------------------------
    #Creates a dictionary of dictionaries. The upper level dicts contain 100 or less dicts that contain query results
    """Returns a QuerySet of all date and non-date variables of the Dataset form combined"""
    def query_every_day(self, graph):
        queries_dict = dict()
        dates = self.create_date_group(graph)
        data = self.query_all(graph)
        queries_dict[0] = data & Data.objects.filter(date_id__in=dates)
        return queries_dict

    """Returns a QuerySet that matches all the non-date attributes of Dataset form"""
    def query_all(self, graph):
        dates = '' #Currently a placeholder, need to add dates implementation to query methods for the time period being queried
        facilities = self.query_facilities(graph, dates)
        area = self.query_area(graph, dates)
        gender = self.query_gender(graph, dates)
        time = self.query_time(graph, dates)
        ret = Data.objects.all()
        if facilities == 'all' and area == 'all' and gender == 'all' and time == 'all':
            return ret
        if not facilities == 'all':
            ret = ret & facilities
        if not area == 'all':
            ret = ret & area
        if not gender == 'all':
            ret = ret & gender
        if not time == 'all':
            ret = ret & time
        return ret

    """Returns a QuerySet that is the period and date queries combined"""
    def create_date_group(self, graph):
        return self.get_period_queries(graph) & self.get_date_queries(graph)

    """Returns a QuerySet of all dates between the start and end date in Dataset form"""
    def get_period_queries(self, graph):
        start = graph.start_date
        end = graph.end_date
        dates = Date.objects.none()
        flag = True
        while (flag):
            if (start == end):
                flag = False
            dates = dates | Date.objects.filter(date=start)
            start += timedelta(days=1)
        dates = dates
        return dates
    
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
    def query_year(self, graph):
        years = self.replace_characters(graph.year)
        ret = Date.objects.none()
        for x in years:
            if x == 'all':
                return 'all'
            ret = ret | Date.objects.filter(year=x)
        return ret
    """Returns a QuerySet of all the months selected in the Dataset form"""
    def query_month(self, graph):
        months = self.replace_characters(graph.month)
        ret = Date.objects.none()
        for x in months:
            if x == 'all':
                return 'all'
            ret = ret | Date.objects.filter(month=x)
        return ret

    """Returns a QuerySet of all the days of the month selected in the Dataset form"""
    def query_day_of_month(self, graph):
        days = self.replace_characters(graph.day_of_month)
        ret = Date.objects.none()
        for x in days:
            if x == 'all':
                return 'all'
            ret = ret | Date.objects.filter(day_of_month=x)
        return ret

    """Returns a QuerySet of all the weeks selected in the Dataset form"""
    def query_week(self, graph):
        weeks = self.replace_characters(graph.week)
        ret = Date.objects.none()
        for x in weeks:
            if x == 'all':
                return 'all'
            ret = ret | Date.objects.filter(week=x)
        return ret

    """Returns a QuerySet of all the days of the week selected in the Dataset form"""
    def query_day_of_week(self, graph):
        days = self.replace_characters(graph.day_of_week)
        ret = Date.objects.none()
        for x in days:
            if x == 'all':
                return 'all'
            ret = ret | Date.objects.filter(day_of_week=x)
        return ret

#Data Queries-------------------------
    """Returns a QuerySet of all the facilities selected in the Dataset form"""
    def query_facilities(self, graph, dates):
        facilities = self.replace_characters(graph.facility)
        ret = Data.objects.none()
        for x in facilities:
            if x == 'all':
                return 'all'
            ret = ret | Data.objects.filter(facility=x)
        return ret

    """Returns a QuerySet of all the areas selected in the Dataset form"""
    def query_area(self, graph, dates):
        areas = self.replace_characters(graph.area)
        ret = Data.objects.none()
        for x in areas:
            if x == 'all':
                return 'all'
            ret = ret | Data.objects.filter(area=x)
        return ret

    """Returns a QuerySet of the gender selected in the Dataset form"""
    def query_gender(self, graph, dates):
        gender = graph.gender
        if gender == 'all':
            return 'all'
        else:
            return Data.objects.filter(gender=gender)

    """Returns a QuerySet of all the times selected in the Dataset form"""
    def query_time(self, graph, dates):
        times = self.replace_characters(graph.time)
        ret = Data.objects.none()
        for x in times:
            if x == 'all':
                return 'all'
            ret = ret | Data.objects.filter(time=x)
        return ret

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

