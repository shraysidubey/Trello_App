# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trello_app', '0006_list_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='created_at',
            field=models.DateTimeField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='card',
            name='created_by',
            field=models.ForeignKey(default=3, to='trello_app.UserProfile'),
            preserve_default=False,
        ),
    ]
