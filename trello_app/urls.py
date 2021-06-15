from django.conf.urls import patterns, url
from trello_app import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = patterns('',
                       url(r'^user/$', views.user, name='user'),
                       url('api-token-auth/$', obtain_auth_token, name='api_token_auth'),
                       url(r'^user/(?P<user_id>[\w\-]+)/$', views.profile, name='profile'),
                       url(r'^bank_details/$', views.bank_details, name='bank_details'),
                       url(r'^board/$', views.board, name='board'),
                       url(r'^board/(?P<board_id>[\w\-]+)/list/$', views.create_lst, name='create_lst'),
                       url(r'^list_details/(?P<list_id>[\w\-]+)/$', views.list_details, name='list_details'),
                       url(r'^list/(?P<lst_id>[\w\-]+)/card/$', views.create_card, name='create_card'),
                       url(r'^card_details/(?P<card_id>[\w\-]+)/$', views.card_details, name='card_details'),
                       url(r'^card/(?P<card_id>[\w\-]+)/attachement/$', views.add_attachements, name='add_attachements'),
                       url(r'^card/(?P<card_id>[\w\-]+)/$', views.deletion_of_card, name='deletion_of_card'),
                       url(r'^card/(?P<card_id>[\w\-]+)/change_position/$', views.change_card_position, name='change_card_position'),
                       url(r'^board_details/(?P<board_id>[\w\-]+)/$', views.board_details, name='board_details'),
                       )