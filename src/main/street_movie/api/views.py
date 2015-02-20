# coding: utf-8

import logging
import json
import sys
import traceback
import decimal
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
            return __response_json(dict(status=1, data=model.as_json))
        except Exception, e:
            logger.error(e)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logger.error(''.join('!! ' + line for line in lines))
            return __response_json(dict(status=0, message=e))

    return __response_json(dict(status=0, message=[(k, v[0]) for k, v in form.errors.items()]))


@add_log()
def detail(request, id):
    try:
        model = Movie.objects.get(id=id)
    except Movie.DoesNotExist, e:
        return __response_json(dict(status=0, message=u'movie not found id = %s ' % id()))
    return __response_json(dict(status=1, data=model.as_json))


def __response_json(dict):
    json_data = json.dumps(dict, ensure_ascii=False, cls=DjangoJSONEncoder)
    return HttpResponse(json_data, content_type='application/json; charset=UTF-8')