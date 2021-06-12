# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trello_app', '0002_auto_20210611_1425'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='card_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='list',
            old_name='lst_title',
            new_name='title',
        ),
        migrations.AddField(
            model_name='board',
            name='created_at',
            field=models.DateTimeField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='list',
            name='created_at',
            field=models.DateTimeField(),
            preserve_default=False,
        ),
    ]
