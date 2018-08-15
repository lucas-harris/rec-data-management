# Generated by Django 2.0.5 on 2018-08-15 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.IntegerField(default=1, max_length=10, primary_key=True, serialize=False)),
                ('type', models.CharField(default='line', max_length=10)),
                ('title', models.CharField(default='title', max_length=50)),
                ('saved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ChartSet',
            fields=[
                ('id', models.IntegerField(default=1, max_length=10, primary_key=True, serialize=False)),
                ('saved', models.BooleanField(default=False)),
                ('name', models.CharField(default='unsaved', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('date', models.DateTimeField(db_index=True, default='2018-01-01', primary_key=True, serialize=False)),
                ('week', models.CharField(default='01', max_length=3)),
                ('year', models.CharField(default='2018', max_length=4)),
                ('month', models.CharField(default='1', max_length=3)),
                ('day_of_week', models.CharField(default='01', max_length=4)),
                ('day_of_month', models.CharField(default='01', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.IntegerField(default=1, max_length=10, primary_key=True, serialize=False)),
                ('color', models.CharField(default='rgb(255, 0, 0, .3', max_length=25)),
                ('label', models.CharField(default='set', max_length=40)),
                ('unit', models.CharField(default='hour', max_length=15)),
                ('facility', models.CharField(default='rec', max_length=20)),
                ('area', models.CharField(default='strength', max_length=20)),
                ('start_date', models.DateTimeField(default='2018-01-01', max_length=20)),
                ('end_date', models.DateTimeField(default='2018-01-01', max_length=20)),
                ('gender', models.CharField(default='rec', max_length=20)),
                ('year', models.CharField(default='2018', max_length=4)),
                ('month', models.CharField(default='January', max_length=2)),
                ('week', models.CharField(default='01', max_length=4)),
                ('day_of_month', models.CharField(default='1', max_length=4)),
                ('day_of_week', models.CharField(default='Monday', max_length=20)),
                ('time', models.CharField(default='0630', max_length=5)),
                ('data_json', models.CharField(default='-', max_length=100000)),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.Chart')),
            ],
        ),
        migrations.RemoveField(
            model_name='datainset',
            name='data',
        ),
        migrations.RemoveField(
            model_name='datainset',
            name='dataset',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='data',
        ),
        migrations.AlterModelOptions(
            name='data',
            options={},
        ),
        migrations.RemoveField(
            model_name='data',
            name='id',
        ),
        migrations.RemoveField(
            model_name='data',
            name='week',
        ),
        migrations.RemoveField(
            model_name='data',
            name='weekday',
        ),
        migrations.AddField(
            model_name='data',
            name='gender',
            field=models.CharField(default='m', max_length=3),
        ),
        migrations.AddField(
            model_name='data',
            name='key',
            field=models.CharField(default='1', max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='data',
            name='time',
            field=models.CharField(default='0630', max_length=5),
        ),
        migrations.AlterField(
            model_name='data',
            name='area',
            field=models.CharField(default='fc', max_length=10),
        ),
        migrations.AlterField(
            model_name='data',
            name='date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.Date'),
        ),
        migrations.AlterField(
            model_name='data',
            name='facility',
            field=models.CharField(default='rec', max_length=10),
        ),
        migrations.AlterField(
            model_name='data',
            name='value',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='DataInSet',
        ),
        migrations.DeleteModel(
            name='Dataset',
        ),
        migrations.AddField(
            model_name='graph',
            name='data',
            field=models.ManyToManyField(to='pages.Data'),
        ),
        migrations.AddField(
            model_name='chart',
            name='chart_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.ChartSet'),
        ),
    ]