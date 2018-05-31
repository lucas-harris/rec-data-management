
from django.db import models
from pages.models import Data
from datetime import *

class DataEntryScript:


    def __init__(self, date, gender, facility, area, time, value):
        self.date = date
        self.gender = gender
        self.facility = facility
        self.area = area
        self.time = time
        self.value = value
        self.id = ''

    def create_data(self):
        self.make_key()
        data = Data(date=self.date, gender=self.gender, facility=self.facility, area=self.area, time=self.time, id=self.id)
        data.save()

    def make_key(self):
        self.date = datetime(int(self.date[6:10]), int(self.date[0:2]), int(self.date[3:5]))
        self.id = str(date.month) + '/' + str(date.day) + '/' + str(date.year) + '-' + self.gender + '-' + self.facility + '-' + self.area + '-' + self.time

