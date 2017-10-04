# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0002_comment_image'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='owner',
            field=models.ManyToManyField(to='profiles.Profile'),
        ),
    ]
