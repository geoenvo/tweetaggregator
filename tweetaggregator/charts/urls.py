from django.conf.urls import url
from . import views


urlpatterns = [
    # /charts/tweet?username=@username
    url(r'^tweet/+(?P<user>[\w,]+)/$', views.index, name='index'),
    url(r'^tweet_charts/+(?P<users>[\w,]+)/$', views.tweet_charts, name='tweet_charts'),
]