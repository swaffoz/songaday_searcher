"""songaday_searcher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.decorators.cache import cache_page

from songs import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', cache_page(60 * 60)(views.index)),
    url(r'^search/(?P<text>[^/|^$]+)/?$', cache_page(60 * 30)(views.search)),
    url(r'^tags/?$', cache_page(60 * 30)(views.tags)),
    url(r'^tags/(?P<text>[^/|^$]+)/?$', cache_page(60 * 30)(views.tags)),
    url(r'^today/?$', cache_page(60 * 30)(views.today)),
    url(r'^songs/?$', cache_page(60 * 30)(views.songs)),
    url(r'^songs/(?P<number>[0-9]+)/?$', cache_page(60 * 30)(views.songs)),
    url(r'^from/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<year>[0-9]{4})/?$', cache_page(60 * 30)(views.from_date)),
    url(r'^lastupdated/?$', views.last_updated),
]
