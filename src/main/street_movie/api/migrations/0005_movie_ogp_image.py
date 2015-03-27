# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20150326_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='ogp_image',
            field=models.FileField(default=None, upload_to=b'%Y/%m/%d', verbose_name='\u52d5\u753b\u30a4\u30e1\u30fc\u30b8'),
            preserve_default=True,
        ),
    ]
