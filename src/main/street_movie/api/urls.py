from django.conf.urls import patterns, include, url

from django.contrib import admin

from api import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^create.json$', views.create, name="street_movie_api_create"),
    url(r'^/(?P<id>\d+).json', views.detail, name="street_movie_api_detail"),
)
