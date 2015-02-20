#-*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse

from django.template import Library

register = Library()


@register.filter
def get_settings(value, args=None):
    if hasattr(settings, value):
        attr = getattr(settings, value)

        if callable(attr):
            return attr()

        if args:
            return attr % args
        return attr


