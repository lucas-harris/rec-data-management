from pages.main.Data import Data
from pages.main.DataSet import DataSet
from pages.main.Chart import Chart
class LineChart(Chart):
    def __init__(self):
        Chart.__init__(self)
        self.datasets = list()
        self.is_stepped = False
        self.is_filled = False
        self.has_points = True
        self.has_lines = True
        self.y_axis_title = ""
        self.x_axis_title = ""

    def get_is_stepped(self):
        return self.is_stepped

    def set_is_stepped(self, flag):
        self.is_stepped = flag

    def get_is_filled(self):
        return self.is_filled

    def set_is_filled(self, flag):
        self.is_filled = flag

    def get_has_points(self):
        return self.has_points

    def set_has_points(self, flag):
        self.has_points = flag

    def get_has_lines(self):
        return self.has_lines

    def set_has_lines(self, flag):
        self.has_lines = flag

    def get_datasets(self):
        return self.datasets

    def add_dataset(self, dataset):
        self.datasets.append(dataset)

    def remove_dataset(self, index):
        self.datasets.pop(index)

    

