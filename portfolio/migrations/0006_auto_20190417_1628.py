# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-17 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_blog'),
    ]

    operations = [
        migrations.CreateModel(
            name='blogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('body', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='blog',
        ),
    ]