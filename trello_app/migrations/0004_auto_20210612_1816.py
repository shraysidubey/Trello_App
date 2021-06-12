# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trello_app', '0003_auto_20210612_1804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='created_at',
            new_name='created_time',
        ),
    ]
