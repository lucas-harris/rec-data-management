# Generated by Django 2.0.5 on 2018-08-15 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20180815_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='chartset',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='graph',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]