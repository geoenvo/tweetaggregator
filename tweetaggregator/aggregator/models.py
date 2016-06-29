from __future__ import unicode_literals

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models
from taggit.managers import TaggableManager

verbose_created = _('Created')
verbose_updated = _('Updated')
verbose_type = _('Type')
verbose_keyword = _('Keyword')
verbose_name = _('Name')
verbose_status = _('Status')
verbose_source = _('Source')
verbose_tweetid = _('Tweet ID')
verbose_tweetcreated = _('Tweet Created')
verbose_tweettext = _('Tweet Text')
verbose_userid = _('User ID')
verbose_username = _('User Name')
verbose_userscreenname = _('User Screen Name')
verbose_userutcoffset = _('User UTC Offset')
verbose_usercoordinate = _('User Coordinate')
verbose_note = _('Note')
verbose_since = _('Since')
verbose_until = _('Until')
verbose_method = _('Method')
verbose_userurl = _('User URL')
verbose_userlocation = _('User Location')
verbose_retweets = _('Retweets')
verbose_favorites = _('Favorites')


class Source(models.Model):
    TYPE_CHOICES = (
        ('TWITTER', _('Twitter')),
    )
    name = models.CharField(
        max_length=100,
        verbose_name=verbose_name
    )
    username = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=verbose_username
    )
    created = models.DateTimeField(
        default=timezone.now,
        verbose_name=verbose_created
    )
    updated = models.DateTimeField(auto_now=True, verbose_name=verbose_updated)
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default='TWITTER',
        verbose_name=verbose_type
    )
    STATUS_CHOICES = (
        ('ACTIVE', _('Active')),
        ('INACTIVE', _('Inactive')),
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='INACTIVE',
        verbose_name=verbose_status
    )
    METHOD_CHOICES = (
        ('TWEEPY', _('TWEEPY')),
        ('GOT', _('GOT')),
    )
    method = models.CharField(
        max_length=50,
        choices=METHOD_CHOICES,
        default='TWEEPY',
        verbose_name=verbose_method
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name=verbose_note
    )
    since = models.DateField(
        blank=True,
        null=True,
        verbose_name=verbose_since
    )
    until = models.DateField(
        blank=True,
        null=True,
        verbose_name=verbose_until
    )

    class Meta:
        ordering = ['pk']
        get_latest_by = 'pk'

    def __unicode__(self):
        return '[%s] - %s' % (self.name, self.status)


class Keyword(models.Model):
    source = models.ForeignKey(
        Source,
        related_name='keywords',
        verbose_name=verbose_source
    )
    keyword = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name=verbose_keyword
    )

    class Meta:
        ordering = ['pk']
        get_latest_by = 'pk'

    def __unicode__(self):
        return '[%s] - %s' % (self.source, self.keyword)


class Twitter(models.Model):
    keyword = models.ForeignKey(
        Keyword,
        related_name='tweets',
        verbose_name=verbose_keyword,
        null=True
    )
    tweet_id = models.BigIntegerField(
        verbose_name=verbose_tweetid
    )
    tweet_created = models.DateTimeField(
        default=timezone.now,
        verbose_name=verbose_tweetcreated
    )
    tweet_text = models.TextField(
        blank=True,
        verbose_name=verbose_tweettext
    )
    user_id = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name=verbose_userid
    )
    user_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=verbose_username
    )
    user_URL = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=verbose_userurl
    )
    user_screen_name = models.CharField(
        max_length=100,
        verbose_name=verbose_userscreenname
    )
    user_utc_offset = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=verbose_userutcoffset
    )
    user_coordinate = models.PointField(
        blank=True,
        null=True,
        verbose_name=verbose_usercoordinate
    )
    user_location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=verbose_userlocation
    )
    retweets = models.IntegerField(
        blank=True,
        default=0,
        verbose_name=verbose_retweets
    )
    favorites = models.IntegerField(
        blank=True,
        default=0,
        verbose_name=verbose_favorites
    )
    tags_tweet = TaggableManager()

    class Meta:
        ordering = ['pk']
        get_latest_by = 'pk'

    def __unicode__(self):
        return '[%s] - %s - %s' % (self.user_name, self.user_screen_name, self.tweet_created)
