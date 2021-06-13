# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trello_app', '0010_attachements_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachements',
            name='link',
            field=models.URLField(default=b'', max_length=520),
        ),
    ]
