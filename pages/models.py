from django.db import models

class Date(models.Model):
    date = models.DateTimeField(primary_key=True, db_index=True, default='2018-01-01')
    week = models.CharField(max_length=3, default='01')
    year = models.CharField(max_length=4, default='2018')
    month = models.CharField(max_length=3, default='1')
    day_of_week = models.CharField(max_length=4, default='01')
    day_of_month = models.CharField(max_length=3, default='01')

    def __str__(self):
        return str(self.date)

class Data(models.Model):
    key = models.CharField(primary_key=True, max_length=50, default='1')
    value = models.IntegerField(default = 0)
    facility = models.CharField(max_length=10, default='rec')
    area = models.CharField(max_length=10, default='fc')
    time = models.CharField(max_length=5, default='0630')
    gender = models.CharField(max_length=3, default='m')
    date = models.ForeignKey(Date, on_delete=models.CASCADE)

class ChartSet(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    saved = models.BooleanField(default=False)
    name = models.CharField(default='unsaved', max_length=60)

class Chart(models.Model):
    id = models.IntegerField(primary_key=True, db_index=False, default=1)
    type = models.CharField(max_length=10, default='line')
    title = models.CharField(max_length=50, default='title')
    chart_set = models.ForeignKey(ChartSet, on_delete=models.CASCADE)
    saved = models.BooleanField(default=False)

class Graph(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE)
    data = models.ManyToManyField('Data')
    color = models.CharField(max_length=25, default='rgb(255, 0, 0, .3')
    label = models.CharField(max_length=60, default='set')
    unit = models.CharField(max_length=15, default='hour')
    facility = models.CharField(max_length=100, default='rec')
    area = models.CharField(max_length=20, default='strength')
    start_date = models.DateTimeField(max_length=20, default='2018-01-01')
    end_date = models.DateTimeField(max_length=500, default='2018-01-01')
    gender = models.CharField(max_length=500, default='rec')
    year = models.CharField(max_length=500, default='2018')
    month = models.CharField(max_length=500, default='January')
    week = models.CharField(max_length=500, default='01')
    day_of_month = models.CharField(max_length=500, default='1')
    day_of_week = models.CharField(max_length=500, default='Monday')
    time = models.CharField(max_length=500, default='0630')
    data_json = models.CharField(max_length=100000, default='-')