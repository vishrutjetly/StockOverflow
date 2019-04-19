# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-19 13:37
from __future__ import unicode_literals

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_remove_stock_meta'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='meta',
            field=django_mysql.models.ListCharField(models.CharField(max_length=20), default=[], max_length=10500, size=500),
            preserve_default=False,
        ),
    ]
