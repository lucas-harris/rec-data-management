# Generated by Django 2.0.5 on 2018-05-24 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='time',
            field=models.CharField(default='630a', max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='data',
            name='date',
            field=models.DateField(),
        ),
    ]
