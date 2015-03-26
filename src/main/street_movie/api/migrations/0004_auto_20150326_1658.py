# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20150326_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='center_lat',
            field=models.DecimalField(default=0.0, verbose_name='\u7def\u5ea6(\u4e2d\u5fc3)', max_digits=9, decimal_places=6),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='center_lon',
            field=models.DecimalField(default=0.0, verbose_name='\u8efd\u5ea6(\u4e2d\u5fc3)', max_digits=9, decimal_places=6),
            preserve_default=True,
        ),
    ]
