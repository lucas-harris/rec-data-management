from pages.main.Data import Data
class DataSet:
    def __init__(self):
        self.dataset = list()

    def get_dataset(self):
        return self.dataset

    def add_data(self, data):
        self.dataset.append(data)
        self.find_common_characteristics()

    def get_data(self, index):
        return self.dataset[index]

    def get_common_characteristics(self):
        return self.common_characteristics

    def get_common_characteristics_string(self):
        returnvalue = ""
        increment = 0
        while increment<len(self.common_characteristics):
            returnvalue += self.common_characteristics[increment]
            increment+=1
        return returnvalue

    def find_common_characteristics(self):
        if len(self.dataset)>0:
            self.common_characteristics = list()
            x = 0
            dateflag = True
            facilityflag = True
            areaflag = True
            timeflag = True
            while x<len(self.dataset)-1:
                if self.dataset[x].get_month()!=self.dataset[x+1].get_month() or self.dataset[x].get_day()!=self.dataset[x+1].get_day() or \
                        self.dataset[x].get_year() != self.dataset[x + 1].get_year():
                    dateflag = False
                if self.dataset[x].get_facility()!=self.dataset[x+1].get_facility():
                    facilityflag = False
                if self.dataset[x].get_area()!=self.dataset[x+1].get_area():
                    areaflag=False
                if self.dataset[x].get_hour()!=self.dataset[x+1].get_hour() or self.dataset[x].get_minute()!=self.dataset[x+1].get_minute():
                    timeflag=False
                x+=1
            if dateflag:
                self.common_characteristics.append(str(self.dataset[0].get_month()) + "/" + str(self.dataset[0].get_day()) + "/" + str(self.dataset[0].get_year()))
            if facilityflag:
                self.common_characteristics.append(self.dataset[0].get_facility())
            if areaflag:
                self.common_characteristics.append(self.dataset[0].get_area())
            if timeflag:
                self.common_characteristics.append(str(self.dataset[0].get_hour()))
                self.common_characteristics.append(str(self.dataset[0].get_minute()))
