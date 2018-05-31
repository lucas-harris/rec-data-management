from pages.main.Data import Data
from pages.main.DataSet import DataSet
from pages.main.Chart import Chart
class CircularChart(Chart):
    def __init__(self):
        Chart.__init__(self)
        self.is_doughnut = False
        self.dataset = None
        self.common_title = ""

    def get_is_doughnut(self):
        return self.is_doughnut

    def set_is_doughnut(self, flag):
        self.is_doughnut = flag

    def get_dataset(self):
        return self.dataset

    def set_dataset(self, dataset):
        self.dataset = dataset

    def set_title(self):
        for x in self.dataset.get_common_characteristics():
            self.common_title += x + " "

chart = CircularChart()
d = Data(5, 1, 1, 2018, "Clawson", "Strength", 10, 30)
e = Data(5, 1, 2, 2018, "Clawson", "Strength", 10, 30)
dset = DataSet()
dset.add_data(d)
dset.add_data(e)
chart.set_dataset(dset)
chart.set_title()
print(chart.common_title)

