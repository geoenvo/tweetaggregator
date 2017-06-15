# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-15 10:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0004_remove_source_property_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitter',
            name='tweet_id',
            field=models.BigIntegerField(db_index=True, verbose_name='Tweet ID'),
        ),
        migrations.AlterField(
            model_name='twitter',
            name='user_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True, verbose_name='User ID'),
        ),
        migrations.AlterField(
            model_name='twitter',
            name='user_screen_name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='User Screen Name'),
        ),
    ]