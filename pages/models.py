from django.db import models

class Date(models.Model):
    date = models.DateTimeField(primary_key=True)
    week = models.CharField(max_length=3)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=3)
    day_of_week = models.CharField(max_length=4)
    day_of_month = models.CharField(max_length=3)

    def __str__(self):
        return str(self.date)

class Data(models.Model):
    key = models.CharField(primary_key=True, max_length=50)
    value = models.IntegerField()
    facility = models.CharField(max_length=10)
    area = models.CharField(max_length=10)
    time = models.CharField(max_length=5)
    gender = models.CharField(max_length=3)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)

    class Meta:
        ordering = ['value']

    def __str__(self):
        return str(self.value)

    def make_key(self):
        return str(self.date) + '-' + str(self.facility) + str(self.area) + '-' + str(self.gender) + '-' + str(self.time)

class ChartSet(models.Model):
    id = models.IntegerField(primary_key=True)

class Chart(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    chart_set = models.ForeignKey(ChartSet, on_delete=models.CASCADE)

class Graph(models.Model):
    id = models.IntegerField(primary_key=True)
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE)
    label = models.ManyToManyField('Data')


class Dataset(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    facility = models.CharField(max_length=20)
    area = models.CharField(max_length=10)
    start_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)
    gender = models.CharField(max_length=6)
    year = models.CharField(max_length=10)
    month = models.CharField(max_length=9)
    week = models.CharField(max_length=10)
    day_of_month = models.CharField(max_length=10)
    day_of_week = models.CharField(max_length=9)
    time = models.CharField(max_length=7)
    units = models.CharField(max_length=10)
    data = models.ManyToManyField(Data, through='DataInSet')
    value = models.IntegerField()


class DataInSet(models.Model):
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)