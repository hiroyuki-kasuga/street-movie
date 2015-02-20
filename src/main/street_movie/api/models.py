# coding: utf-8

import time
from django.conf import settings
from django.db import models


class Movie(models.Model):
    movie = models.FileField(
        u"動画",
        upload_to='%Y/%m/%d'
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


