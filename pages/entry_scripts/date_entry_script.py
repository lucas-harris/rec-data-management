from datetime import *
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
        self.week = self.date.strftime("%V")

    def create_date(self):
        self.create_fields()
        d = Date(date=self.date, day_of_month=self.day_of_month, month=self.month, day_of_week=self.day_of_week, week=self.week, year=self.year)
        d.save()
