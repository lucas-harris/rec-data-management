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
    estimated = models.BooleanField(default = False)

class ChartSet(models.Model):
    id = models.IntegerField(primary_key=True)
    saved = models.BooleanField(default=False)
    name = models.CharField(default='unsaved', max_length=60)

class Chart(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=10, default='line')
    title = models.CharField(max_length=50)
    chart_set = models.ForeignKey(ChartSet, on_delete=models.CASCADE)
    saved = models.BooleanField(default=False)

class Graph(models.Model):
    id = models.IntegerField(primary_key=True)
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE)
    data = models.ManyToManyField('Data')
    color = models.CharField(max_length=25, default='rgb(255, 0, 0, .3')
    label = models.CharField(max_length=40, default='set')
    unit = models.CharField(max_length=15, default='hour')
    facility = models.CharField(max_length=20, default='rec')
    area = models.CharField(max_length=20, default='strength')
    start_date = models.DateTimeField(max_length=20, default='2018-01-01')
    end_date = models.DateTimeField(max_length=20, default='2018-01-01')
    gender = models.CharField(max_length=20, default='rec')
    year = models.CharField(max_length=4, default='2018')
    month = models.CharField(max_length=2, default='January')
    week = models.CharField(max_length=4, default='01')
    day_of_month = models.CharField(max_length=4, default='1')
    day_of_week = models.CharField(max_length=20, default='Monday')
    time = models.CharField(max_length=5, default='0630')
    data_json = models.CharField(max_length=100000, default='')