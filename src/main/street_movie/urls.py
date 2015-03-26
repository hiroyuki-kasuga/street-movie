from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'web.views.index', name="street_movie_site_views_index"),
    url(r'^ogp/(?P<m_id>\d+)/$', 'web.views.ogp', name="street_movie_site_views_ogp"),
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
