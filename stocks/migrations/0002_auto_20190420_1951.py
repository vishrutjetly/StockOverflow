# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-20 19:51
from __future__ import unicode_literals

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='meta',
            field=django_mysql.models.ListCharField(models.CharField(max_length=20), blank=True, max_length=10500, size=500),
        ),
        migrations.AddField(
            model_name='stock',
            name='meta_predict',
            field=django_mysql.models.ListCharField(models.CharField(max_length=20), blank=True, max_length=10500, size=500),
        ),
        migrations.AddField(
            model_name='stock',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
