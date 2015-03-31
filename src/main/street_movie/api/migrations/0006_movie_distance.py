# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_movie_ogp_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='distance',
            field=models.IntegerField(default=0, verbose_name='\u8ddd\u96e2'),
            preserve_default=True,
        ),
    ]
