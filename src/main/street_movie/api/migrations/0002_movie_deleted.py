# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='\u524a\u9664\u30d5\u30e9\u30b0'),
            preserve_default=True,
        ),
    ]
