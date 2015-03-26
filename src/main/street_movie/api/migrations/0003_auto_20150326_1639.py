# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_movie_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='end_name',
            field=models.TextField(default=None, verbose_name='\u30a8\u30f3\u30c9\u5730\u70b9'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='start_name',
            field=models.TextField(default=None, verbose_name='\u30b9\u30bf\u30fc\u30c8\u5730\u70b9'),
            preserve_default=True,
        ),
    ]
