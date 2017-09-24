# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(max_length=500, null=True)),
                ('albums', models.ManyToManyField(blank=True, null=True, to='albums.Album')),
            ],
        ),
    ]
