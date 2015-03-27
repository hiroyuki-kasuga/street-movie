# coding: utf-8

import time
from django.conf import settings
from django.db import models
import storages.backends.s3boto


class ApiCount(models.Model):
    target_date = models.DateField(
        u'対象日',
    )

    counter = models.IntegerField(
        u'APIカウント',
    )

    created_at = models.DateTimeField(
        u"登録日時",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        u"更新日時",
        auto_now=True
    )

    class Meta:
        db_table = u'api_count'
        verbose_name = u'APIカウント'
        verbose_name_plural = u'APIカウント'


class Movie(models.Model):
    movie = models.FileField(
        u"動画",
        upload_to='%Y/%m/%d'
    )

    ogp_image = models.FileField(
        u"動画イメージ",
        upload_to='%Y/%m/%d',
        default=None,
        storage=storages.backends.s3boto.S3BotoStorage(
            acl='public-read'
        )
    )

    start_lat = models.DecimalField(
        u"緯度(スタート)",
        max_digits=9,
        decimal_places=6,
        default=0.000000
    )

    start_lon = models.DecimalField(
        u"軽度(スタート)",
        max_digits=9,
        decimal_places=6,
        default=0.000000
    )

    end_lat = models.DecimalField(
        u"緯度(エンド)",
        max_digits=9,
        decimal_places=6,
        default=0.000000
    )

    end_lon = models.DecimalField(
        u"軽度(エンド)",
        max_digits=9,
        decimal_places=6,
        default=0.000000
    )

    center_lat = models.DecimalField(
        u"緯度(中心)",
        max_digits=9,
        decimal_places=6,
        default=0.000000
    )

    center_lon = models.DecimalField(
        u"軽度(中心)",
        max_digits=9,
        decimal_places=6,
        default=0.000000
    )

    start_name = models.TextField(
        u'スタート地点',
        default=None
    )

    end_name = models.TextField(
        u'エンド地点',
        default=None
    )

    deleted = models.BooleanField(
        u'削除フラグ',
        default=False,
    )

    created_at = models.DateTimeField(
        u"登録日時",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        u"更新日時",
        auto_now=True
    )

    class Meta:
        db_table = u'street_movie'
        verbose_name = u'動画'
        verbose_name_plural = u'動画'

    @property
    def as_json(self):
        import pytz

        updated_at = self.updated_at.astimezone(pytz.timezone(settings.TIME_ZONE))
        updated_at = time.mktime(updated_at.timetuple())
        created_at = self.created_at.astimezone(pytz.timezone(settings.TIME_ZONE))
        created_at = time.mktime(created_at.timetuple())

        return dict(id=self.id, movie=self.movie.url, start_lat=self.start_lat, start_lon=self.start_lon,
                    end_lat=self.end_lat, end_lon=self.end_lon, created_at=created_at, updated_at=updated_at)


