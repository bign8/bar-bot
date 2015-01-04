from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    url(r'^test$', views.test),
    url(r'^create$', views.create, name='create'),
)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
