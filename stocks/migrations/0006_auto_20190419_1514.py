# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-19 15:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0005_stock_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='meta',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='updated_at',
        ),
    ]