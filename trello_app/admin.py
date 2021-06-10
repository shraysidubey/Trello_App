from django.contrib import admin

from trello_app.models import UserProfile, Board, List, Card, Bank

admin.site.register(UserProfile)

admin.site.register(Board)

admin.site.register(List)

admin.site.register(Card)

admin.site.register(Bank)