import calendar
from collections import OrderedDict
from functools import cmp_to_key

from django import forms
from .models import *
from datetime import *

class Query():

#Sort Results
    def sort_results(self, form):
        dictionary = self.group_queries(form)
        return_dictionary = OrderedDict()
        inc = form.cleaned_data['units']
        if inc=='day':
            for key in sorted(dictionary, key=cmp_to_key(self.compare_day)):
                return_dictionary[key] = dictionary[key]
        elif inc=='hour':
            for key in sorted(dictionary, key=cmp_to_key(self.compare_hour)):
                return_dictionary[key] = dictionary[key]
        elif inc=='week':
            for key in sorted(dictionary, key=cmp_to_key(self.compare_week)):
                return_dictionary[key] = dictionary[key]
        elif inc=='month':
            for key in sorted(dictionary, key=cmp_to_key(self.compare_month)):
                return_dictionary[key] = dictionary[key]
        elif inc=='year':
            for key in sorted(dictionary):
                return_dictionary[key] = dictionary[key]
        return return_dictionary


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

    def compare_week(self, week1, week2):
        if week1[9:13] <= week2[9:13]:
            if week1[5:7] < week2[5:7]:
                return -1
            else:
                return 1
        else:
            return 1

    def compare_day(self, day1, day2):
        if day1[6:10] <= day2[6:10]:
            if day1[0:2] <= day2[0:2]:
                if day1[3:5] < day2[3:5]:
                    return -1
                else:
                    return 1
            else:
                return 1
        else:
            return 1

    def compare_hour(self, hour1, hour2):
        day_check = False #Checks if hour1's day comes before/equals hour2's
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



#Combination of Queries-------------------------
    def query_every_day(self, form):
        return_query = Data.objects.none()
        dates = self.create_date_group(form)
        size = len(dates)
        queries_dict = dict()
        index = 0
        dict_index = 0
        for x in range(0,size):
            if index == 100:
                index = 0
                dict_index += 1
            if not dict_index in queries_dict:
                queries_dict[dict_index] = Data.objects.none()
            queries_dict[dict_index] = queries_dict[dict_index] | self.query_all(form, dates[x].date)
            index += 1
        # for key in queries_dict:
        #     return_query = return_query | queries_dict[key]
        return queries_dict

    def query_all(self, form, date):
        return self.query_facilities(form, date) & self.query_area(form, date) & self.query_gender(form, date) & self.query_time(form, date)

    def create_date_group(self, form):
        return self.get_period_queries(form) & self.get_date_queries(form)

    def get_period_queries(self, form):
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']
        dates = Date.objects.none()
        flag = True
        while (flag):
            if (start == end):
                flag = False
            dates = dates | Date.objects.filter(date=start)
            start += timedelta(days=1)
        dates = dates
        return dates

    def get_date_queries(self, form):
        return self.query_month(form) & self.query_week(form)  & self.query_year(form) & self.query_day_of_month(form) & self.query_day_of_week(form)


#Date Queries-------------------------
    def query_year(self, form):
        ret = Date.objects.none()
        for x in form.cleaned_data['year']:
            if x == 'all':
                return Date.objects.all()
            ret = ret | Date.objects.filter(year=x)
        return ret

    def query_month(self, form):
        ret = Date.objects.none()
        for x in form.cleaned_data['month']:
            if x == 'all':
                return Date.objects.all()
            ret = ret | Date.objects.filter(month=x)
        return ret

    def query_day_of_month(self, form):
        ret = Date.objects.none()
        for x in form.cleaned_data['day_of_month']:
            if x == 'all':
                return Date.objects.all()
            ret = ret | Date.objects.filter(day_of_month=x)
        return ret

    def query_week(self, form):
        ret = Date.objects.none()
        for x in form.cleaned_data['week']:
            if x == 'all':
                return Date.objects.all()
            ret = ret | Date.objects.filter(week=x)
        return ret

    def query_day_of_week(self, form):
        ret = Date.objects.none()
        for x in form.cleaned_data['day_of_week']:
            if x == 'all':
                return Date.objects.all()
            ret = ret | Date.objects.filter(day_of_week=x)
        return ret

#Data Queries-------------------------
    def query_facilities(self, form, date):
        ret = Date.objects.get(date=date).data_set.none()
        for x in form.cleaned_data['facility']:
            if x == 'all':
                return Date.objects.get(date=date).data_set.all()
            ret = ret | Date.objects.get(date=date).data_set.filter(facility=x)
        return ret

    def query_area(self, form, date):
        ret = Date.objects.get(date=date).data_set.none()
        for x in form.cleaned_data['area']:
            if x == 'all':
                return Date.objects.get(date=date).data_set.all()
            ret = ret | Date.objects.get(date=date).data_set.filter(area=x)
        return ret

    def query_gender(self, form, date):
        ret = Date.objects.get(date=date).data_set.none()
        if form.cleaned_data['gender'] == 'all':
            return Date.objects.get(date=date).data_set.all()
        else:
            ret = ret | Date.objects.get(date=date).data_set.filter(gender=form.cleaned_data['gender'])
        return ret

    def query_time(self, form, date):
        ret = Date.objects.get(date=date).data_set.none()
        for x in form.cleaned_data['time']:
            if x == 'all':
                return Date.objects.get(date=date).data_set.all()
            ret = ret | Date.objects.get(date=date).data_set.filter(time=x)
        return ret


#Increment Grouping

    def group_queries(self, form):
        inc = form.cleaned_data['units']
        if inc=='year':
            return self.group_by_year(self.query_every_day(form))
        elif inc=='month':
            return self.group_by_month(self.query_every_day(form))
        elif inc=='week':
            return self.group_by_week(self.query_every_day(form))
        elif inc=='day':
            return self.group_by_day(self.query_every_day(form))
        elif inc=='hour':
            return self.group_by_hour(self.query_every_day(form))

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

    def make_year_key(self, data):
        return str(data.date.year)

    def group_by_month(self, dictionary):
        month_dict = OrderedDict()
        for key in dictionary:
            for x in dictionary[key]:
                if self.make_month_key(x) in month_dict:
                    value = month_dict[self.make_month_key(x)] + x.value
                else:
                    month_dict[self.make_month_key(x)] = 0
                    value = x.value
                month_dict[self.make_month_key(x)] =  value
        return month_dict

    def make_month_key(self, data):
        return calendar.month_name[int(data.date.month)] + ' ' + str(data.date.year)

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

    def make_week_key(self, data):
        return 'Week ' + data.date.week + ', ' + str(data.date.year)

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