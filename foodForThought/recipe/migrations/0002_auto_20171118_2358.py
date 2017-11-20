# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-18 23:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipelName', models.CharField(max_length=250)),
                ('cuisine', models.CharField(max_length=250)),
                ('recipeProcedure', models.CharField(max_length=1000000)),
            ],
        ),
        migrations.AlterField(
            model_name='ingredientlist',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.RecipeD'),
        ),
        migrations.DeleteModel(
            name='Recipe',
        ),
    ]
