"""tweetaggregator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView
import taggit_autosuggest.urls


admin_url_pattern = [url(r'^admin/', admin.site.urls)]

if getattr(settings, 'ADMIN_URL_PATTERN', False):
    admin_url_pattern = [url(getattr(settings, 'ADMIN_URL_PATTERN'), admin.site.urls)]

urlpatterns = admin_url_pattern + [
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='home'),
    # url(r'^admin/', admin.site.urls),
    url(r'^charts/', include('charts.urls')),
    url(r'^twitter/', include('twitter.urls')),
    url(r'^taggit_suggest/', include('taggit_autosuggest.urls')),
]


# Allow dev server to serve media files
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif getattr(settings, 'FORCE_SERVE_STATIC', False): # If set to True force dev server to serve static files
    settings.DEBUG = True
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    settings.DEBUG = False

# Change admin header text
if getattr(settings, 'ADMIN_SITE_HEADER', False):
    admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER')
if getattr(settings, 'ADMIN_INDEX_TITLE', False):
    admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE')
if getattr(settings, 'ADMIN_SITE_TITLE', False):
    admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE')
