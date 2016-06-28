from django.conf.urls import url
from . import views


urlpatterns = [
    # /charts/tweet?username=@username
    #url(r'^$', views.index, name='index'),
    url(r'^tweet/+(?P<user>\w+)/$', views.index, name='index'),
]