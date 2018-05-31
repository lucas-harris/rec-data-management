from pages.main.Data import Data
from pages.main.DataSet import DataSet
from pages.main.Chart import Chart
class ScatterPlot(Chart):
    def __init__(self):
        Chart.__init__(self)
        self.dataset1 = None
        self.dataset2 = None

    def get_dataset1(self):
        return self.dataset1

    def set_dataset1(self, dataset):
        self.dataset1 = dataset

    def get_dataset2(self):
        return self.dataset2

    def set_dataset2(self, dataset):
        self.dataset2 = dataset