# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-02-23 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0002_auto_20190223_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='size',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='age',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='size',
            field=models.CharField(max_length=10),
        ),
    ]