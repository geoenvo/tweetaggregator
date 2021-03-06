# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 17:57
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Retweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('retweet_id', models.BigIntegerField(verbose_name='Retweet ID')),
                ('retweet_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Tweet Created')),
                ('user_id', models.BigIntegerField(blank=True, null=True, verbose_name='User ID')),
                ('user_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='User Name')),
                ('user_URL', models.CharField(blank=True, max_length=100, null=True, verbose_name='User URL')),
                ('user_screen_name', models.CharField(max_length=100, verbose_name='User Screen Name')),
                ('user_utc_offset', models.IntegerField(blank=True, null=True, verbose_name='User UTC Offset')),
                ('user_coordinate', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='User Coordinate')),
                ('followers_count', models.BigIntegerField(default=0, verbose_name='Followers')),
                ('following_count', models.BigIntegerField(default=0, verbose_name='Following')),
                ('favorites', models.IntegerField(blank=True, default=0, verbose_name='Favorites')),
                ('tweet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.Twitter', verbose_name='Tweet ID')),
            ],
            options={
                'ordering': ['pk'],
                'get_latest_by': 'pk',
            },
        ),
        migrations.CreateModel(
            name='Source_Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Tweet Created')),
                ('followers_count', models.BigIntegerField(default=0, verbose_name='Followers')),
                ('following_count', models.BigIntegerField(default=0, verbose_name='Following')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='aggregator.Source', verbose_name='Source')),
            ],
            options={
                'ordering': ['pk'],
                'get_latest_by': 'pk',
            },
        ),
    ]
