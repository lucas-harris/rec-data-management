import datetime
from datetime import timedelta
from pages.models import Date
from django.db import models

class DateEntryScript:
    
    def __init__(self, date):
        self.date = date
        self.day_of_month = ''
        self.month = ''
        self.day_of_week = ''
        self.week = ''
        self.year = ''

    def create_fields(self):
        self.day_of_month = self.date.day
        self.month = self.date.month
        self.year = self.date.year
        self.day_of_week = self.date.weekday()
        self.week = self.create_week(self.year, self.date)
    
    def create_week(self, year, date_to_add):
        week_dict = {1:'01', 2:'02', 3:'03', 4:'04', 5:'05', 6:'06', 7:'07', 8:'08', 9:'09', 
        10:'10', 11:'11', 12:'12', 13:'13', 14:'14', 15:'15', 16:'16', 17:'17', 18:'18', 19:'19', 
        20:'20', 21:'21', 22:'22', 23:'23', 24:'24', 25:'25', 26:'26', 27:'27', 28:'28', 29:'29', 
        30:'30', 31:'31', 32:'32', 33:'33', 34:'34', 35:'35', 36:'36', 37:'37', 38:'38', 39:'39',
        40:'40', 41:'41', 42:'42', 43:'43', 44:'44', 45:'45', 46:'46', 47:'47', 48:'48', 49:'49',
        50:'50', 51:'51', 52:'52'  
        }
        if date_to_add >= datetime.datetime(year, 7, 1):
            date = datetime.datetime(year, 7, 1)
            while date.weekday() != 0:
                if date_to_add == date:
                    return week_dict[52]
                date += timedelta(days=1)
            week = 1
            day = 0
            while date < date_to_add:
                date += timedelta(days=1)
                day += 1
                if day == 7:
                    week += 1
                    day = 0
            return week_dict[week]
        else:
            date = datetime.datetime(year-1, 7, 1)
            while date.weekday() != 0:
                date += timedelta(days=1)
            week = 1
            day = 0
            while date < date_to_add:
                date += timedelta(days=1)
                day += 1
                if day == 7:
                    week += 1
                    day = 0
            return week_dict[week]


    def create_date(self):
        self.create_fields()
        d = Date(date=self.date, day_of_month=self.day_of_month, month=self.month, day_of_week=self.day_of_week, week=self.week, year=self.year)
        d.save()
