# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-19 14:07
from __future__ import unicode_literals

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0003_stock_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='meta',
            field=django_mysql.models.ListCharField(models.CharField(max_length=20), blank=True, max_length=10500, size=500),
        ),
    ]