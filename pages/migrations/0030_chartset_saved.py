# Generated by Django 2.0.5 on 2018-06-11 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0029_auto_20180608_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='chartset',
            name='saved',
            field=models.BooleanField(default=False),
        ),
    ]