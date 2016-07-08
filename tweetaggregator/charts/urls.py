from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^tweet/+(?P<users>[\w,]+)/$', views.tweet_charts, name='tweet_charts'),
]