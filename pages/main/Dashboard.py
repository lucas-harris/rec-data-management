from pages.main.Data import Data
from pages.main.DataSet import DataSet
from pages.main.Chart import Chart
from pages.main.LineChart import LineChart
from pages.main.BarChart import BarChart
from pages.main.CircularChart import CircularChart
from pages.main.ScatterPlot import ScatterPlot

class Dashboard:
    def __init__(self):
        self.charts = list()
        self.width = 1

    def add_chart(self, chart):
        chart.set_index(len(self.charts))
        self.charts.append(chart)

    def delete_chart(self, index):
        self.charts.pop(index)

    def swap_chart(self, index1, index2):
        chart_to_swap = self.charts[index1]
        self.charts[index1] = self.charts[index2]
        self.charts[index2] = chart_to_swap

    def get_width(self):
        return self.width

    def set_width(self, new_width):
        self.width = new_width

data1 = Data(10, 2, 28, 2020, "rec", "strength", 10, 30)
data2 = Data(20, 2, 28, 2020, "clawson", "strength", 10, 30)
data3 = Data(30, 2, 28, 2020, "north quad", "strength", 10, 30)
dataset1 = DataSet()
dataset1.add_data(data1)
dataset1.add_data(data2)
dataset1.add_data(data3)