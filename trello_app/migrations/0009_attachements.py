# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trello_app', '0008_auto_20210613_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachements',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attached_at', models.DateTimeField()),
                ('card', models.ForeignKey(to='trello_app.Card')),
                ('user_profile', models.ForeignKey(to='trello_app.UserProfile', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
