# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-19 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_auto_20190419_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
