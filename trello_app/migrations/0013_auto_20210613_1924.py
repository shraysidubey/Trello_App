# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trello_app', '0012_auto_20210613_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.URLField(default=b'', max_length=520)),
                ('attached_at', models.DateTimeField()),
                ('card', models.ForeignKey(to='trello_app.Card')),
                ('user_profile', models.ForeignKey(to='trello_app.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='attachements',
            name='card',
        ),
        migrations.RemoveField(
            model_name='attachements',
            name='user_profile',
        ),
        migrations.DeleteModel(
            name='Attachements',
        ),
    ]
