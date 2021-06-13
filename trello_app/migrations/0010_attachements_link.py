# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trello_app', '0009_attachements'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachements',
            name='link',
            field=models.URLField(default=2, max_length=520),
            preserve_default=False,
        ),
    ]
