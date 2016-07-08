from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.all_user, name='all_user'),
    url(r'^users/+(?P<user>[\w]+)/$', views.all_crawled_user, name='all_crawled_user'),
]