from __future__ import unicode_literals

from django.utils.translation import gettext_lazy as _
from django.contrib.gis import admin

from .models import Source, Keyword, Twitter


verbose_source_details = _('Source details')
verbose_twitter_details = _('Twitter details')
verbose_keyword_details = _('Keyword details')


class KeywordInline(admin.TabularInline):
    model = Keyword
    extra = 3


class SourceAdmin(admin.ModelAdmin):
    fieldsets = [
        (verbose_source_details, {
            'fields': [
                'method',
                'username',
                ('since', 'until'),
                'name',
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
        'type',
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
                'user_id',
                'tweet_created',
                'tweet_id',
                'tweet_text',
                'user_utc_offset',
                'user_coordinate'
            ]
        })
    ]
    list_display = [
        'keyword',
        'user_screen_name',
        'tweet_id',
        'tweet_created'
    ]
    ordering = ['-tweet_created']
    date_hierarchy = 'tweet_created'
    list_filter = ['keyword', 'tweet_created', 'user_name']
    search_fields = ['user_name', 'keyword', 'user_screen_name', 'tweet_text']


admin.site.register(Source, SourceAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Twitter, TwitterAdmin)
