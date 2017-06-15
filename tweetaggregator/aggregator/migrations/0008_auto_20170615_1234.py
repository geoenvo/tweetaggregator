# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-15 12:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0007_twitter_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='source_property',
            options={'get_latest_by': 'pk', 'ordering': ['pk'], 'verbose_name_plural': 'Source Properties'},
        ),
        migrations.AlterModelOptions(
            name='twitter',
            options={'get_latest_by': 'pk', 'ordering': ['pk'], 'verbose_name_plural': 'Twitter'},
        ),
    ]
