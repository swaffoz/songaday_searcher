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
from songs import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^search/(?P<text>[^/|^$]+)/?$', views.search),
    url(r'^tags/?$', views.tags),
    url(r'^tags/(?P<text>[^/|^$]+)/?$', views.tags),
    url(r'^today/?$', views.today),
    url(r'^songs/?$', views.songs),
    url(r'^songs/(?P<number>[0-9]+)/?$', views.songs),
    url(r'^from/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<year>[0-9]{4})/?$', views.from_date),
    url(r'^lastupdated/?$', views.last_updated),
]
