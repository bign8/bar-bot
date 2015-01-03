from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('www.urls', namespace='www')),
)
