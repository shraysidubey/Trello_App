# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trello_app', '0005_auto_20210612_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='created_by',
            field=models.ForeignKey(default=1, to='trello_app.UserProfile'),
            preserve_default=False,
        ),
    ]
