# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trello_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='user_profile',
            field=models.ForeignKey(default=0, to='trello_app.UserProfile', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bank',
            name='card_holder_name',
            field=models.CharField(max_length=200),
        ),
    ]
