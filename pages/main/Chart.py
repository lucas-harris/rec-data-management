from pages.main.DataSet import DataSet
from pages.main.Data import Data

class Chart:
    def __init__(self):
        self.title = "title"
        self.color_list = list()
        self.categories = list()
        self.index = -1

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_color(self, index):
        return self.color_list[index]

    def add_color(self, red, green, blue):
        self.color_list.append([red, green, blue])

    def change_color(self, index, red, green, blue):
        self.color_list[index] = [red, green, blue]

    def get_color_list(self):
        return self.color_list

    def get_categories(self):
        return self.categories

    def add_category(self, category):
        self.categories.append(category)

    def remove_category(self, index):
        self.categories.pop(index)

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index





