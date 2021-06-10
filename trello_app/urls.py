from django.conf.urls import patterns, url
from trello_app import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = patterns('',
        url(r'^user/$', views.user, name='user'),
        url('api-token-auth/$', obtain_auth_token, name='api_token_auth'),
        url(r'^user/(?P<user_id>[\w\-]+)/$', views.profile, name='profile'),
                       )
