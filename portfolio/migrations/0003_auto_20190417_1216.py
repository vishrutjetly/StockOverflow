# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-17 12:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolio', '0002_pf_inst'),
    ]

    operations = [
        migrations.CreateModel(
            name='pf_inst2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('x', models.TextField()),
                ('y', models.TextField()),
                ('pf_user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='pf_inst',
        ),
    ]
