# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target_date', models.DateField(verbose_name='\u5bfe\u8c61\u65e5')),
                ('counter', models.IntegerField(verbose_name='API\u30ab\u30a6\u30f3\u30c8')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u767b\u9332\u65e5\u6642')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65e5\u6642')),
            ],
            options={
                'db_table': 'api_count',
                'verbose_name': 'API\u30ab\u30a6\u30f3\u30c8',
                'verbose_name_plural': 'API\u30ab\u30a6\u30f3\u30c8',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('movie', models.FileField(upload_to=b'%Y/%m/%d', verbose_name='\u52d5\u753b')),
                ('start_lat', models.DecimalField(default=0.0, verbose_name='\u7def\u5ea6(\u30b9\u30bf\u30fc\u30c8)', max_digits=9, decimal_places=6)),
                ('start_lon', models.DecimalField(default=0.0, verbose_name='\u8efd\u5ea6(\u30b9\u30bf\u30fc\u30c8)', max_digits=9, decimal_places=6)),
                ('end_lat', models.DecimalField(default=0.0, verbose_name='\u7def\u5ea6(\u30a8\u30f3\u30c9)', max_digits=9, decimal_places=6)),
                ('end_lon', models.DecimalField(default=0.0, verbose_name='\u8efd\u5ea6(\u30a8\u30f3\u30c9)', max_digits=9, decimal_places=6)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u767b\u9332\u65e5\u6642')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65e5\u6642')),
            ],
            options={
                'db_table': 'street_movie',
                'verbose_name': '\u52d5\u753b',
                'verbose_name_plural': '\u52d5\u753b',
            },
            bases=(models.Model,),
        ),
    ]
