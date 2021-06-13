# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('trello_app', '0007_auto_20210613_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='due_date',
            field=models.DateTimeField(default=datetime.date(2021, 6, 13)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='description',
            field=models.TextField(default=b'', max_length=300),
        ),
    ]
