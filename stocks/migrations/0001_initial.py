# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-19 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('ticker', models.CharField(max_length=10)),
                ('meta', django_mysql.models.ListCharField(models.CharField(max_length=20), max_length=10500, size=500)),
            ],
        ),
    ]
