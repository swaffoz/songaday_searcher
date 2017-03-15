import json
import datetime

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError
from django.core import serializers
from django.contrib.postgres.search import TrigramSimilarity
from django.utils import timezone

from .models import Song, Tag, SongUpdateToken


def index(request):
    data = {'help': 'See API documentation here: ' +
            'https://github.com/zaneswafford/songaday_searcher/blob/master/API.md'}
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
        song = Song.objects.get(release_date=timezone.now().date())
    except Song.DoesNotExist:
        return HttpResponseNotFound(content_type='application/json')
    else:
        data = serializers.serialize(
            "json", [song], use_natural_foreign_keys=True)
        return HttpResponse(data, content_type='application/json')

def latest(request):
    try:
        song = Song.objects.order_by('-release_date')[0]
    except IndexError:
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


def last_updated(request):
    try:
        update_token = SongUpdateToken.objects.last()
        update_token_dict = {'started': str(update_token.started),
                             'finished': str(update_token.finished),
                             'songs_updated': update_token.song_count}
        data = json.dumps(update_token_dict)
    except Exception as e:
        return HttpResponseServerError(content_type='application/json')
    else:
        return HttpResponse(data, content_type='application/json')
