from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^trello_app/api/v1/', include('trello_app.urls')),
)
