from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.conf import settings
from django.conf.urls.static import static
from . import views

admin.site.site_header = 'Young Space Administration'

urlpatterns = [
    url(r'^user(?P<action>(/[a-z]*)*)', views.user),
    url(r'^event(?P<action>(/[a-z]*)*)', views.event),
    url(r'^admin', admin.site.urls),
    url(r'^about', views.about),
    url(r'^$', views.index)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
