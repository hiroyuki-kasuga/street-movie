# coding: utf-8

import logging
import json
import sys
import traceback
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder

from django.http import HttpResponse
from api.forms import CreateMovieForm
from api.models import Movie
from api.services import CreateMovieService

from decorator.decorators import add_log

logger = logging.getLogger(__name__)


@add_log()
def create(request):
    form = CreateMovieForm(request.POST)
    if form.is_valid():
        lat_lng_list = json.loads(form.cleaned_data['latLng'])
        create_service = CreateMovieService()
        try:
            model = create_service.create_movie(lat_lng_list, form)
            model_json = model.as_json
            model_json['sns_url'] = request.build_absolute_uri(
                reverse('street_movie_site_views_ogp', kwargs={'m_id': model.id}))
            model_json['sns_title'] = settings.FB_OGP_TITLE
            create_service.save_count()
            model_json['count'] = create_service.get_count()
            return __response_json(dict(status=1, data=model_json))
        except Exception, e:
            create_service.save_count()
            logger.error(e)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logger.error(''.join('!! ' + line for line in lines))
            return __response_json(dict(status=0))

    return __response_json(dict(status=0))


@add_log()
def detail(request, m_id):
    try:
        model = Movie.objects.get(id=m_id)
    except Movie.DoesNotExist, e:
        return __response_json(dict(status=0))
    return __response_json(dict(status=1, data=model.as_json))


@add_log()
def count(request):
    service = CreateMovieService()
    return __response_json(dict(status=1, data={'count': service.get_count()}))


def __response_json(dict):
    json_data = json.dumps(dict, ensure_ascii=False, cls=DjangoJSONEncoder)
    return HttpResponse(json_data, content_type='application/json; charset=UTF-8')