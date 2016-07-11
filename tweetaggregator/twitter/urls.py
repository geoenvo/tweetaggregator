from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.all_user, name='all_user'),
    url(r'^users/tweets/$', views.all_crawled_tweets, name='all_crawled_tweets'),
    url(r'^users/+(?P<user>[\w]+)/$', views.all_crawled_user, name='all_crawled_user'),
]