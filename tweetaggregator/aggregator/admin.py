from __future__ import unicode_literals

from django.utils.translation import gettext_lazy as _
from django.contrib.gis import admin
from django.contrib.admin import SimpleListFilter

from .forms import TwitterForm
from .models import Source, Keyword, Twitter, Retweet, Source_Property, Category


verbose_source_details = _('Source details')
verbose_twitter_details = _('Twitter details')
verbose_keyword_details = _('Keyword details')
verbose_retweet_details = _('Retweet details')
verbose_source_property_details = _('Source Property details')


class KeywordInline(admin.TabularInline):
    model = Keyword
    extra = 3


class SourceAdmin(admin.ModelAdmin):
    fieldsets = [
        (verbose_source_details, {
            'fields': [
                'method',
                'type',
                'name',
                'username',
                ('since', 'until'),
                'created',
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


# For filtering tweets based on categories field
class CategoryFilter(SimpleListFilter):
    """
    Custom filter by tweets categories. For multiple category queries separate category keywords with comma.
    """
    title = 'Category'
    parameter_name = 'categories'

    def lookups(self, request, model_admin):
        categories = Category.objects.all()
        return [(category.name, category.name) for category in categories]

    def queryset(self, request, queryset):
        if self.value():
            # check if multiple categories are joined by comma and search articles that have all categories
            categories = [category.strip() for category in self.value().split(',')]
            if len(categories) > 1:
                for category in categories:
                    queryset = queryset.filter(categories__icontains=category)
                return queryset
            else:
                return queryset.filter(categories__icontains=self.value())
        else:
            return queryset


class TwitterAdmin(admin.ModelAdmin):
    form = TwitterForm
    fieldsets = [
        (verbose_twitter_details, {
            'fields': [
                'keyword',
                'categories',
                'published',
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
        'user_screen_name',
        'tweet_created',
        'url_',
        'retweets',
        'favorites',
        'keyword',
        'categories',
        'published',
        ####'tags',
        ####'user_coordinate'
    ]
    ordering = ['-tweet_created']
    date_hierarchy = 'tweet_created'
    list_editable = ['published',]
    list_filter = [
      'keyword',
      'tweet_created',
      CategoryFilter,
      ####'user_screen_name'
    ]
    search_fields = [
        ####'user_name',
        'user_screen_name',
        'tweet_created',
        'tweet_text'
    ]

    def tags(self, twitter):
        tags = []
        for tag in twitter.tags_tweet.all():
            tags.append(str(tag))
        return ', '.join(tags)

    def url_(self, instance):
        return '<a href="{url}" target="_blank">{title}</a>'.format(
            url=instance.url, title=instance.url)
    url_.allow_tags = True


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
                'followers_count',
                'following_count',
                'favorites'
            ]
        })
    ]
    list_display = [
        'tweet_id',
        'user_screen_name',
        'followers_count',
        'following_count',
        'favorites',
        'retweet_created'
    ]
    ordering = ['-retweet_created']
    date_hierarchy = 'retweet_created'
    list_filter = ['tweet_id', 'user_screen_name', 'retweet_created']
    search_fields = ['user_name', 'user_screen_name', 'retweet_id', 'retweet_created']


class SourcePropertyAdmin(admin.ModelAdmin):
    fieldsets = [
        (verbose_source_property_details, {
            'fields': [
                'source',
                'created',
                'followers_count',
                'following_count'
            ]
        })
    ]
    list_display = [
        'source',
        'created',
        'followers_count',
        'following_count'
    ]
    list_filter = ['source__name', 'source__username', 'source__method']
    search_fields = ['source__name', 'source__username', 'source__method', 'created']


# For managing tweet categories
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]


admin.site.register(Source, SourceAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Twitter, TwitterAdmin)
admin.site.register(Retweet, RetweetAdmin)
admin.site.register(Source_Property, SourcePropertyAdmin)
admin.site.register(Category, CategoryAdmin)
