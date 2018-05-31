from pages.main.Data import Data
from pages.main.DataSet import DataSet
from pages.main.Chart import Chart
class BarChart(Chart):
    def __init__(self):
        Chart.__init__(self)
        self.bar_width = 1.0
        self.is_horizontal = False
        self.y_axis_title = ""
        self.x_axis_title = ""
        self.dataset = None
        self.common_title = ""

    def get_is_horizontal(self):
        return self.is_horizontal

    def set_is_horizontal(self, flag):
        self.is_horizontal = flag

    def get_y_axis_title(self):
        return self.y_axis_title

    def set_y_axis_title(self, title):
        self.y_axis_title = title

    def get_x_axis_title(self):
        return self.x_axis_title

    def set_x_axis_title(self, title):
        self.x_axis_title = title

    def get_bar_width(self):
        return self.bar_width

    def set_bar_width(self, width):
        self.bar_width = width

    def get_dataset(self):
        return self.dataset

    def set_dataset(self, dataset):
        self.dataset = dataset

    def set_title(self):
        for x in self.dataset.get_common_characteristics():
            self.common_title += x + " "




d = Data(10, 1, 1, 2018, "rec", "strength", 10, 30)
dd = Data(10, 1, 1, 2018, "clawson", "strength", 10, 30)
dset = DataSet()
dset.add_data(d)
dset.add_data(dd)
c = BarChart()
c.add_color(255, 0, 0)
c.set_dataset(dset)
c.set_title()
print(c.title)