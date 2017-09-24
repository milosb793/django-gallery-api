# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, height_field=150, null=True, upload_to='../static/img', verbose_name='Profile picture', width_field=150),
        ),
    ]
