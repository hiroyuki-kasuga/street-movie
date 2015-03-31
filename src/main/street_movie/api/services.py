# coding: utf-8
import commands

import logging, urllib2
import os
import tempfile
import traceback
import sys
import uuid
import math
import binascii
import datetime
from django.conf import settings
from django.core.files import File
from api.models import Movie, ApiCount
from decorator.decorators import interceptor

logger = logging.getLogger(__name__)


@interceptor
class CreateMovieService:
    def __init__(self):
        self.movie_thumbnail_list = []
        self.dir_path = tempfile.mkdtemp()
        self.count = 0

    def get_movie(self, m_id):
        return Movie.objects.get(id=m_id)

    def get_count(self):
        try:
            model = ApiCount.objects.get(target_date=datetime.datetime.now().strftime("%Y-%m-%d"))
        except ApiCount.DoesNotExist:
            return 0
        return model.counter

    def save_count(self):
        try:
            model = ApiCount.objects.get(target_date=datetime.datetime.now().strftime("%Y-%m-%d"))
        except ApiCount.DoesNotExist:
            model = ApiCount()
            model.counter = self.count
            model.target_date = datetime.datetime.now().strftime("%Y-%m-%d")
            model.save()
        else:
            model.counter += self.count
            model.save()

    def create_movie(self, json, form):

        i = 0
        for k, j in enumerate(json):
            try:
                self.__get_street_view_image(j, i)
                i += 1
            except urllib2.HTTPError, e:
                if e.code == 403:
                    continue

        # directory 査走 & ファイル名のソート
        file_list = self.__list_dir_and_sort()
        # バイナリ比較 & 同じものを削除
        self.__diff_file_and_remove(file_list)
        # 再付番
        self.__re_numbered()

        file_name = str(uuid.uuid4()) + '.mp4'
        dest = os.path.join(settings.MOVIE_DEST_PATH, file_name)
        command = settings.FFMPEG_COMMAND % (self.dir_path, dest)
        (status, output) = commands.getstatusoutput(command)
        if status == 0:
            ogp_file, ogp_file_name = self.__get_ogp_image(form)
            model = Movie()
            model.start_lat = form.cleaned_data['start_lat']
            model.start_lon = form.cleaned_data['start_lon']
            model.end_lat = form.cleaned_data['end_lat']
            model.end_lon = form.cleaned_data['end_lon']
            model.start_name = form.cleaned_data['start_name']
            model.end_name = form.cleaned_data['end_name']
            model.center_lat = form.cleaned_data['center_lat']
            model.center_lon = form.cleaned_data['center_lon']
            model.movie.save(file_name, File(open(dest)))
            model.ogp_image.save(ogp_file_name, File(open(ogp_file)))
            model.save()
            os.remove(ogp_file)
            os.remove(dest)
            return model
        raise OSError(status, output)

    def __list_dir_and_sort(self):
        file_list = []
        for f in os.listdir(self.dir_path):
            if '.jpg' in f:
                file_list.append(f)

        file_list.sort()

        ret = []
        for f in file_list:
            ret.append(os.path.join(self.dir_path, f))
        return ret

    def __diff_file_and_remove(self, file_list):
        for i, f in enumerate(file_list):
            if not os.path.exists(f):
                continue
            for j, f1 in enumerate(file_list):
                if not os.path.exists(f1) or i == j:
                    continue
                of = open(f, 'rb')
                of1 = open(f1, 'rb')
                bf = binascii.hexlify(of.read())
                bf1 = binascii.hexlify(of1.read())
                of.close()
                of1.close()
                if bf == bf1:
                    os.remove(f1)

    def __re_numbered(self):
        file_list = []
        for f in os.listdir(self.dir_path):
            if '.jpg' in f:
                file_list.append(f)
        file_list.sort()

        for i, f in enumerate(file_list):
            os.rename(os.path.join(self.dir_path, f), '%s/%05d.jpg' % (self.dir_path, i))

    def __get_ogp_image(self, form):
        url = settings.FB_OGP_IMAGE % (
            form.cleaned_data['center_lat'], form.cleaned_data['center_lon'], form.cleaned_data['start_lat'],
            form.cleaned_data['start_lon'], form.cleaned_data['end_lat'], form.cleaned_data['end_lon'])
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
        file_name = str(uuid.uuid4()) + '.jpg'
        file = os.path.join(self.dir_path, file_name)
        f = open(file, "wb")
        f.write(response.read())
        f.close()
        return file, file_name

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
            self.count = self.count + 1
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


