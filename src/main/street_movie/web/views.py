# coding: utf-8
import logging
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.template import loader

from django.views.decorators.csrf import csrf_exempt
from api.models import Movie
from api.services import CreateMovieService
from decorator.decorators import add_log

logger = logging.getLogger(__name__)


@csrf_exempt
@add_log()
def index(request):
    service = CreateMovieService()
    model = None
    if 'id' in request.GET:
        try:
            model = service.get_movie(request.GET['id'])
            model = model.as_json
            model['sns_url'] = request.build_absolute_uri(
                reverse('street_movie_site_views_ogp', kwargs={'m_id': model['id']}))
        except Movie.DoesNotExist:
            pass

    service = CreateMovieService()
    count = service.get_count()
    c = RequestContext(request, {'count': count, 'model': model})
    t = loader.get_template('web/index.html')
    return HttpResponse(t.render(c))


@csrf_exempt
@add_log()
def ogp(request, m_id):
    service = CreateMovieService()
    try:
        model = service.get_movie(m_id)
    except Movie.DoesNotExist:
        raise Http404

    url = request.build_absolute_uri(reverse('street_movie_site_views_ogp', kwargs={'m_id': model.id}))
    next_url = request.build_absolute_uri(reverse('street_movie_site_views_index')) + '?id=' + m_id

    description = settings.FB_OGP_DESCRIPTION % (model.start_name, model.end_name, model.distance/1000, settings.MAP_SPEED)
    ogp = dict(title=settings.FB_OGP_TITLE, description=description, next_url=next_url, url=url,
               app_id=settings.FB_APP_ID, image=model.ogp_image.url)

    c = RequestContext(request, {'ogp': ogp})
    t = loader.get_template('web/ogp.html')
    return HttpResponse(t.render(c))


