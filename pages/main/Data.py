from datetime import datetime, tzinfo
class Data:
    def __init__(self, value, month, day, year, facility, area, hour, minute):
        self.value = value
        self.date = datetime(year, month, day, hour, minute, 0, 0)
        self.week = self.date.isocalendar()[1]
        self.weekday = self.date.weekday()
        self.facility = facility
        self.area = area
        self.all_characteristics = ""
        self.unique_characteristics = ""
    def make_all_characteristics(self):
        return [self.date.month, self.date.day, self.date.year, self.facility, self.area, self.date.hour, self.date.minute]
    def make_characteristics_string(self):
        return str(self.date.month)+ "/" + str(self.date.day) + "/" + str(self.date.year) + ", " + self.facility + ", " + self.area + ", " + str(self.date.hour) + ":" + str(self.date.minute)
    def get_value(self):
        return self.value
    def get_date(self):
        return self.date
    def get_month(self):
        return self.date.month
    def get_day(self):
        return self.date.day
    def get_year(self):
        return self.date.year
    def get_week(self):
        return self.week
    def get_facility(self):
        return self.facility
    def get_area(self):
        return self.area
    def get_hour(self):
        return self.date.hour
    def get_minute(self):
        return self.date.minute
    def set_unique_characteristics(self, unique):
        self.unique_characteristics = unique
    def get_unique_characteristics(self):
        return self.unique_characteristics






