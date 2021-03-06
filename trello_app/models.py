from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):     # created --> if object of user(any model) is not created it will give you false
    if created:
        Token.objects.create(user=instance)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    alias = models.CharField(max_length=50)
    workplace_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.alias


class Board(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=300)
    created_at = models.DateTimeField()

    def __unicode__(self):
        return self.title


class List(models.Model):
    board = models.ForeignKey(Board)
    created_by = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=300)
    created_at = models.DateTimeField()

    def __unicode__(self):
        return self.title


class Card(models.Model):
    list = models.ForeignKey(List)
    created_by = models.ForeignKey(UserProfile)
    created_at = models.DateTimeField()
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=300, default="")
    due_date = models.DateTimeField()
    position = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class Bank(models.Model):
    user_profile = models.ForeignKey(UserProfile, unique=True)
    card_holder_name = models.CharField(max_length=200)
    cvv = models.IntegerField()
    expiry_date = models.DateTimeField()

    def __unicode__(self):
        return self.card_holder_name


class Attachement(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    card = models.ForeignKey(Card)
    link = models.URLField(max_length=520, default="")
    attached_at = models.DateTimeField()

    def __unicode__(self):
        return self.link


