import json
import re
import yapi
import urllib.request

from enum import Enum
from django.conf import settings


class Column(Enum):
    SONG_NUMBER = 1
    RELEASE_DATE = 2
    TITLE = 3
    URL = 4
    DOWNLOAD_URL = 5
    TAGS = 6
    DESCRIPTION = 7


def jsonp_to_dict(jsonp):
    return json.loads(re.sub(r'([a-zA-Z_0-9\.]*\()|(\);?$)', '', jsonp))


def youtube_id_from_url_string(url_string):
    try:
        youtube_id = url_string.split('/')[-1].split('=')[-1]
        if 'youtu' not in url_string or not youtube_id:
            raise Exception()

    except Exception as e:
        raise Exception(
            'URL String {} is not a youtube video url.'.format(url_string))
    else:
        return youtube_id


def songs_from_spreadsheet(spreadsheet_dict):
    songs = []
    song = None

    for entry in spreadsheet_dict['entry']:
        cell = entry['gs$cell']
        data = cell['$t']
        row = int(cell['row'])
        column = int(cell['col'])

        if row <= 1:
            continue

        if Column(column) == Column.SONG_NUMBER:
            if song and 'song_number' in song and 'title' in song and 'url' in song:
                songs.append(song)
            song = {'song_number': int(re.sub("[^0-9]", "", data))}

        elif Column(column) == Column.RELEASE_DATE:
            song['release_date'] = data

        elif Column(column) == Column.TITLE:
            song['title'] = data

        elif Column(column) == Column.URL:
            song['url'] = data
            try:
                song['youtube_id'] = youtube_id_from_url_string(data)
            except Exception as e:
                print(e)

        elif Column(column) == Column.DOWNLOAD_URL:
            song['download_url'] = data

        elif Column(column) == Column.TAGS:
            song['tags'] = [tag.strip()
                            for tag in data.split(',') if tag.strip()]

        elif Column(column) == Column.DESCRIPTION:
            song['description'] = data

    return songs


def fetch_songs_from_spreadsheet(spreadsheet_url):
    songs = []
    req = urllib.request.Request(spreadsheet_url)
    with urllib.request.urlopen(req) as response:
        jsonp_response = str(response.read(), 'utf-8')
        sheet = jsonp_to_dict(jsonp_response)['feed']
        songs = songs_from_spreadsheet(sheet)
    return songs


def song_metadata_from_youtube_video_item(yt_video):
    metadata = {}

    metadata['youtube_id'] = yt_video.id
    metadata['description'] = yt_video.snippet.description
    metadata['view_count'] = yt_video.statistics.viewCount

    if hasattr(yt_video.snippet, 'likeCount'):
        metadata['like_count'] = yt_video.statistics.likeCount

    if hasattr(yt_video.snippet, 'dislikeCount'):
        metadata['dislike_count'] = yt_video.statistics.dislikeCount

    if hasattr(yt_video.snippet, 'tags'):
        metadata['tags'] = yt_video.snippet.tags

    if yt_video.snippet.thumbnails.default:
        metadata['thumbnail_url'] = yt_video.snippet.thumbnails.default.url

    return metadata


def update_song_with_metadata_dict(song, metadata_dict):
    song['description'] = metadata_dict.get('description')
    song['view_count'] = metadata_dict.get('view_count')
    song['like_count'] = metadata_dict.get('like_count')
    song['dislike_count'] = metadata_dict.get('dislike_count')
    song['thumbnail_url'] = metadata_dict.get('thumbnail_url')

    if 'tags' in metadata_dict:
        song.setdefault('tags', []).extend(metadata_dict.get('tags'))

    return song


def fetch_youtube_metadata_for_songs(songs):
    updated_songs = []
    unmodified_songs = songs
    youtube_ids = [song['youtube_id']
                   for song in songs if song.get('youtube_id')]

    max_ids_per_query = 50
    id_chunks = [youtube_ids[x:x + max_ids_per_query]
                 for x in range(0, len(youtube_ids), max_ids_per_query)]

    video_items = []
    for ids in id_chunks:
        try:
            api = yapi.YoutubeAPI(settings.YOUTUBE_API_KEY)
            video_items = video_items + api.get_video_list_info(ids).items
        except AttributeError as e:
            raise Exception(
                'Unable to query Youtube API. Possibly over quota.')

    for item in video_items:
        metadata = song_metadata_from_youtube_video_item(item)
        song = [song for song in unmodified_songs if song.get(
            'youtube_id') == metadata.get('youtube_id')][0]
        updated_songs.append(
            update_song_with_metadata_dict(song, metadata))
        unmodified_songs.remove(song)

    return updated_songs + unmodified_songs
