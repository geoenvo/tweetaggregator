# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 18:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0003_source_property_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source_property',
            name='user_name',
        ),
    ]
