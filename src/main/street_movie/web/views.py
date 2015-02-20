# coding: utf-8
import logging
from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader

from django.views.decorators.csrf import csrf_exempt
from decorator.decorators import add_log

logger = logging.getLogger(__name__)

@csrf_exempt
@add_log()
def index(request):
    c = RequestContext(request, {})
    t = loader.get_template('web/index.html')
    return HttpResponse(t.render(c))


