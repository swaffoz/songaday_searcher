import datetime

from django.utils import timezone
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from .fetch_songs import fetch_songs_from_spreadsheet, fetch_youtube_metadata_for_songs
from .models import Song, Tag, SongUpdateToken


@periodic_task(run_every=(crontab(minute='*/30')), name="fetch_and_update_songs")
def fetch_and_update_songs():
    token = SongUpdateToken.objects.create(started=timezone.now())

    songs = fetch_songs_from_spreadsheet('https://spreadsheets.google.com/feeds/cells/' +
                                         '1HRfMfK1IF3sP9tTmBe_eXClBuG-Go9BCXmFK9oipSvA' +
                                         '/od6/public/values?alt=json-in-script')

    print('Fetched {} songs'.format(len(songs)))

    updated_songs = fetch_youtube_metadata_for_songs(songs)

    print('Got youtube metadata for {} songs'.format(len(updated_songs)))

    for song_dict in updated_songs:
        update_song_from_dict(song_dict)

    print('Updated Songs in Database')

    token.finished = timezone.now()
    token.song_count = len(updated_songs)
    token.save()


def song_from_number(song_number):
    song = None
    try:
        song = Song.objects.get(song_number=song_number)
    except Song.DoesNotExist as e:
        song = Song(song_number=song_number)
    finally:
        return song


def update_song_from_dict(song_dict):
    song = song_from_number(song_dict.get('song_number'))

    song.title = song_dict.get('title')
    song.description = song_dict.get('description')
    song.url = song_dict.get('url')
    song.download_url = song_dict.get('download_url')
    song.view_count = song_dict.get('view_count')
    song.like_count = song_dict.get('like_count')
    song.dislike_count = song_dict.get('dislike_count')
    song.thumbnail_url = song_dict.get('thumbnail_url')

    release_date = song_dict.get('release_date')
    if release_date:
        song.release_date = datetime.datetime.strptime(
            release_date, '%m/%d/%Y').date()

    song.save()

    tags = song_dict.get('tags')
    if tags:
        [song.tags.add(tag_from_string(tag)) for tag in tags if tag]

    song.save()


def tag_from_string(s):
    tag = None
    try:
        tag = Tag.objects.get(text=s.lower())
    except Tag.DoesNotExist:
        tag = Tag.objects.create(text=s.lower())
    finally:
        return tag
