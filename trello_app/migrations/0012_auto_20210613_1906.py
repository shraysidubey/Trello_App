# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trello_app', '0011_auto_20210613_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachements',
            name='user_profile',
            field=models.ForeignKey(to='trello_app.UserProfile'),
        ),
    ]
