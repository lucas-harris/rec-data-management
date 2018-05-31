from datetime import datetime
class LineInterval:
    def __init__(self, start_date, end_date, start_hour, start_minute, end_hour, end_minute, unit_of_measure):
        self.start = datetime(self.parse_date(start_date)[2], self.parse_date(start_date)[0], self.parse_date(start_date)[1], start_hour, start_minute, 0, 0)
        self.end = datetime(self.parse_date(end_date)[2], self.parse_date(end_date)[0], self.parse_date(end_date)[1], end_hour, end_minute, 0, 0)
        self.unit_of_measure = unit_of_measure

    def get_start(self):
        return self.start

    def set_start(self, date):
        self.start = date
            
    def get_end(self):
        return self.end

    def set_end(self, date):
        self.end = date

    def parse_date(self, date):
        return date[0:2], date[3:5], date[6:10]

