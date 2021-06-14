# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trello_app', '0013_auto_20210613_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='position',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
