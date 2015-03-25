# coding: utf-8
import commands

import logging, urllib2
import os
import tempfile
import traceback
import sys
import uuid
import math
from django.conf import settings
from django.core.files import File
from api.models import Movie
from decorator.decorators import interceptor

logger = logging.getLogger(__name__)


@interceptor
class CreateMovieService:
    def __init__(self):
        self.movie_thumbnail_list = []
        self.dir_path = tempfile.mkdtemp()

    def create_movie(self, json, form):

        i = 0
        for k, j in enumerate(json):
            try:
                self.__get_street_view_image(j, i)
                i = i + 1
            except urllib2.HTTPError, e:
                if e.code == 403:
                    continue

        file_name = str(uuid.uuid4()) + '.mp4'
        dest = os.path.join(settings.MOVIE_DEST_PATH, file_name)
        command = settings.FFMPEG_COMMAND % (self.dir_path, dest)
        (status, output) = commands.getstatusoutput(command)
        if status == 0:
            model = Movie()
            model.movie.save(file_name, File(open(dest)))
            model.start_lat = form.cleaned_data['start_lat']
            model.start_lon = form.cleaned_data['start_lon']
            model.end_lat = form.cleaned_data['end_lat']
            model.end_lon = form.cleaned_data['end_lon']
            model.save()
            os.remove(dest)
            return model
        raise OSError(status, output)

    def __get_street_view_image(self, json, i):

        heading = ''
        if 'radius' in json:
            heading = '&heading=' + str(json['radius'])

        url = settings.STREET_VIEW_URL % (json['lat'], json['lng'], settings.GOOGLE_API_KEY, heading)

        logger.debug('google url %s' % url)
        request = urllib2.Request(url)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            logger.error(e)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logger.error(''.join('!! ' + line for line in lines))
            raise e
        except urllib2.URLError, e:
            logger.error(e)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logger.error(''.join('!! ' + line for line in lines))
            raise e
        else:
            file = '%s/%05d.jpg' % (self.dir_path, i)
            f = open(file, "wb")
            f.write(response.read())
            f.close()
            self.movie_thumbnail_list.append(file)

    def __direction(self, lat1, lng1, lat2, lng2):
        Y = math.cos(lng2 * math.pi / 180) * math.sin(lat2 * math.pi / 180 - lat1 * math.pi / 180)
        X = math.cos(lng1 * math.pi / 180) * math.sin(lng2 * math.pi / 180) - math.sin(lng1 * math.pi / 180) * math.cos(
            lng2 * math.pi / 180) * math.cos(lat2 * math.pi / 180 - lat1 * math.pi / 180)
        dirE0 = 180 * math.atan2(Y, X) / math.pi
        if dirE0 < 0:
            dirE0 = dirE0 + 360
        dirN0 = (dirE0 + 180) % 360
        return dirN0


