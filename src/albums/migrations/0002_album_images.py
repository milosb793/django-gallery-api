# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('albums', '0001_initial'),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='album_images', to='images.Image'),
        ),
    ]
