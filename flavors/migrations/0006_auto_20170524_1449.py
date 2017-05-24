# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-24 21:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flavors', '0005_auto_20170518_1938'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserComboData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('dislike', models.BooleanField(default=False)),
                ('favorite', models.BooleanField(default=False)),
                ('note', models.CharField(blank=True, max_length=500)),
                ('combination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flavors.Combination')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='combination',
            name='users',
            field=models.ManyToManyField(through='flavors.UserComboData', to=settings.AUTH_USER_MODEL),
        ),
    ]
