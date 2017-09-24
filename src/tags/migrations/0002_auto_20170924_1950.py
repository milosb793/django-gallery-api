# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 19:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20170924_1937'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='images',
        ),
        migrations.AddField(
            model_name='tag',
            name='images',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='images.Image'),
        ),
    ]
