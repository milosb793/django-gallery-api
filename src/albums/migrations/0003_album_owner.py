# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 21:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('albums', '0002_album_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile'),
        ),
    ]
