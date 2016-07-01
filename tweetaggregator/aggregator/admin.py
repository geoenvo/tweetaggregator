from __future__ import unicode_literals

from django.utils.translation import gettext_lazy as _
from django.contrib.gis import admin

from .models import Source, Keyword, Twitter, Retweet


verbose_source_details = _('Source details')
verbose_twitter_details = _('Twitter details')
verbose_keyword_details = _('Keyword details')
verbose_retweet_details = _('Retweet details')


class KeywordInline(admin.TabularInline):
    model = Keyword
    extra = 3


class SourceAdmin(admin.ModelAdmin):
    fieldsets = [
        (verbose_source_details, {
            'fields': [
                'method',
                'name',
                'username',
                ('since', 'until'),
                'created',
                'type',
                'status',
                'note'
            ]
        })
    ]
    list_display = [
        'name',
        'created',
        'updated',
        'username',
        'method',
        'status'
    ]
    readonly_fields = ['updated']
    ordering = ['-updated', '-created']
    date_hierarchy = 'created'
    list_filter = ['created', 'type', 'status', 'method']
    search_fields = ['name', 'type', 'note']
    inlines = [KeywordInline]


class KeywordAdmin(admin.ModelAdmin):
    fieldsets = [
        (verbose_keyword_details, {
            'fields': [
                'source',
                'keyword'
            ]
        })
    ]
    list_display = [
        'source',
        'keyword'
    ]
    list_filter = ['source__name']
    search_fields = ['keyword', 'source__name']


class TwitterAdmin(admin.ModelAdmin):
    fieldsets = [
        (verbose_twitter_details, {
            'fields': [
                'keyword',
                'user_name',
                'user_screen_name',
                'tags_tweet',
                'user_URL',
                'user_id',
                'tweet_created',
                'tweet_id',
                'tweet_text',
                'retweets',
                'favorites',
                'user_utc_offset',
                'user_coordinate',
                'user_location'
            ]
        })
    ]
    list_display = [
        'tweet_id',
        'keyword',
        'tags',
        'user_screen_name',
        'retweets',
        'favorites',
        'user_coordinate',
        'tweet_created'
    ]
    ordering = ['-tweet_created']
    date_hierarchy = 'tweet_created'
    list_filter = ['keyword', 'tweet_created', 'user_name']
    search_fields = ['user_name', 'keyword', 'user_screen_name', 'tweet_text']

    def tags(self, twitter):
        tags = []
        for tag in twitter.tags_tweet.all():
            tags.append(str(tag))
        return ', '.join(tags)


class RetweetAdmin(admin.ModelAdmin):
    fieldsets = [
        (verbose_retweet_details, {
            'fields': [
                'tweet_id',
                'user_name',
                'user_screen_name',
                'retweet_id',
                'retweet_created',
                'user_id',
                'user_URL',
                'user_utc_offset',
                'user_coordinate',
                'retweets',
                'favorites'
            ]
        })
    ]
    list_display = [
        'tweet_id',
        'user_screen_name',
        'favorites',
        'retweet_created'
    ]
    ordering = ['-retweet_created']
    date_hierarchy = 'retweet_created'
    list_filter = ['tweet_id', 'user_screen_name', 'retweet_created']
    search_fields = ['user_name', 'user_screen_name', 'tweet_id', 'retweet_id', 'retweet_created']


admin.site.register(Source, SourceAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Twitter, TwitterAdmin)
admin.site.register(Retweet, RetweetAdmin)
