# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trello_app', '0004_auto_20210612_1816'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='created_time',
            new_name='created_at',
        ),
    ]
