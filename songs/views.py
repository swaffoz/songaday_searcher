import json
import datetime

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.core import serializers
from django.contrib.postgres.search import TrigramSimilarity

from .models import Song, Tag


def index(request):
    data = {'response': 'Help message goes here'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def search(request, text=None):
    try:
        similarities = TrigramSimilarity(
            'title', text) + TrigramSimilarity('description', text)
        songs = Song.objects.annotate(
            similarity=similarities,
        ).filter(similarity__gte=0.1).order_by('-similarity')
        assert(len(songs) > 0)
    except AssertionError:
        return HttpResponseNotFound(content_type='application/json')
    else:
        data = serializers.serialize(
            "json", songs, use_natural_foreign_keys=True)
        return HttpResponse(data, content_type='application/json')


def tags(request, text=None):
    if not text:
        tags = Tag.objects.all()
        data = serializers.serialize("json", tags)
        return HttpResponse(data, content_type='application/json')

    try:
        songs = Song.objects.filter(tags__text__in=[text])
        assert(len(songs) > 0)
    except AssertionError:
        return HttpResponseNotFound(content_type='application/json')
    else:
        data = serializers.serialize(
            "json", songs, use_natural_foreign_keys=True)
        return HttpResponse(data, content_type='application/json')


def today(request):
    try:
        song = Song.objects.get(release_date=datetime.date.today())
    except Song.DoesNotExist:
        return HttpResponseNotFound(content_type='application/json')
    else:
        data = serializers.serialize(
            "json", [song], use_natural_foreign_keys=True)
        return HttpResponse(data, content_type='application/json')


def from_date(request, month=None, day=None, year=None):
    try:
        song_date = datetime.date(int(year), int(month), int(day))
        song = Song.objects.get(release_date=song_date)
        data = serializers.serialize(
            "json", [song], use_natural_foreign_keys=True)
    except Song.DoesNotExist:
        return HttpResponseNotFound(content_type='application/json')
    except Exception as e:
        return HttpResponseBadRequest(content_type='application/json')
    else:
        return HttpResponse(data, content_type='application/json')


def songs(request, number=None):
    if not number:
        songs = Song.objects.all()
        data = serializers.serialize("json", songs, fields=[
                                     'title', 'song_number', 'release_date'])
        return HttpResponse(data, content_type='application/json')

    try:
        song = Song.objects.get(song_number=number)
        data = serializers.serialize(
            "json", [song], use_natural_foreign_keys=True)
    except Song.DoesNotExist:
        return HttpResponseNotFound(content_type='application/json')
    else:
        return HttpResponse(data, content_type='application/json')
