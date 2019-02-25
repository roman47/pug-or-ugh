# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-02-23 19:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0003_auto_20190223_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdog',
            name='dog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pugorugh.Dog'),
        ),
        migrations.AlterField(
            model_name='userdog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]