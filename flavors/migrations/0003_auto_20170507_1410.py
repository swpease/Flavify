# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-07 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flavors', '0002_auto_20170505_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taste',
            name='mouth_taste',
            field=models.CharField(choices=[('sweet', 'Sweet'), ('salty', 'Salty'), ('sour', 'Sour'), ('bitter', 'Bitter'), ('umami', 'Umami'), ('spicy', 'Spicy'), ('numbing', 'Numbing'), ('cooling', 'Cooling')], max_length=20),
        ),
    ]
