# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 03:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_auto_20171118_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='reciped',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
    ]
