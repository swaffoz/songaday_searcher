import yapi

from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from songs import fetch_songs


class FetchSongsTestCase(TestCase):

    def test_column_enum_values_are_correct(self):
        """
        The Spreadsheet Column Enum should have columns in the following order:
        Song Number, Release Date, Song Title, Video URL, Download URL, Tags, Description
        """
        self.assertEqual(fetch_songs.Column(1), fetch_songs.Column.SONG_NUMBER)
        self.assertEqual(fetch_songs.Column(
            2), fetch_songs.Column.RELEASE_DATE)
        self.assertEqual(fetch_songs.Column(3), fetch_songs.Column.TITLE)
        self.assertEqual(fetch_songs.Column(4), fetch_songs.Column.URL)
        self.assertEqual(fetch_songs.Column(
            5), fetch_songs.Column.DOWNLOAD_URL)
        self.assertEqual(fetch_songs.Column(6), fetch_songs.Column.TAGS)
        self.assertEqual(fetch_songs.Column(7), fetch_songs.Column.DESCRIPTION)

    def test_column_enum_rejects_invalid_column(self):
        """
        The Spreadsheet Column Enum should raise an error if presented with a column 
        that is greater than 7 or less than 1
        """
        with self.assertRaises(ValueError):
            fetch_songs.Column(0)

        with self.assertRaises(ValueError):
            fetch_songs.Column(8)

    def test_jsonp_to_dict_returns_valid_dict_from_jsonp_string(self):
        """
        The JSONP to Dict method should strip the padding off and give us a valid python
        dict with all the appropriate values
        """
        jsonp_str = 'jsonCallback({"dogs":[{"name":"Bo","breed":"Black Lab"}]});'
        expected_result = {"dogs": [{"name": "Bo", "breed": "Black Lab"}]}
        result = fetch_songs.jsonp_to_dict(jsonp_str)

        self.assertEqual(result, expected_result)

    def test_youtube_id_from_url_string_returns_correct_id(self):
        url = 'https://www.youtube.com/watch?v=hQVTIJBZook'
        expected_result = 'hQVTIJBZook'
        result = fetch_songs.youtube_id_from_url_string(url)

        self.assertEqual(result, expected_result)

    def test_youtube_id_from_url_string_raises_on_non_youtube_url(self):
        url = "https://vimeo.com/v=123"

        with self.assertRaises(Exception):
            fetch_songs.youtube_id_from_url_string(url)

    def test_songs_from_spreadsheet_returns_complete_song_dicts(self):
        spreadsheet_dict = {'entry': [
            {'gs$cell': {'$t': 'ColumnHeader', 'row': '1', 'col': '1'}},
            {'gs$cell': {'$t': '12345', 'row': '2', 'col': '1'}},
            {'gs$cell': {'$t': '12/30/2016', 'row': '2', 'col': '2'}},
            {'gs$cell': {'$t': 'Test Song', 'row': '2', 'col': '3'}},
            {'gs$cell': {'$t': 'https://youtu.be/hQVTIJBZook', 'row': '2', 'col': '4'}},
            {'gs$cell': {'$t': 'http://downlo.ad/12345', 'row': '2', 'col': '5'}},
            {'gs$cell': {'$t': 'fun, folk, happy', 'row': '2', 'col': '6'}},
            {'gs$cell': {'$t': 'This is test', 'row': '2', 'col': '7'}},
            {'gs$cell': {'$t': '12346', 'row': '3', 'col': '1'}}
        ]}

        expected_result = [{
            'song_number': 12345,
            'release_date': '12/30/2016',
            'title': 'Test Song',
            'url': 'https://youtu.be/hQVTIJBZook',
            'download_url': 'http://downlo.ad/12345',
            'tags': ['fun', 'folk', 'happy'],
            'description': 'This is test',
            'youtube_id': 'hQVTIJBZook'
        }]
        result = fetch_songs.songs_from_spreadsheet(spreadsheet_dict)

        self.assertEqual(result, expected_result)

    def test_update_song_with_metadata_dict_updates_required_values(self):
        song = {
            'song_number': 12345,
            'release_date': '12/30/2016',
            'title': 'Test Song',
            'url': 'https://youtu.be/hQVTIJBZook',
            'download_url': 'http://downlo.ad/12345',
            'tags': ['fun', 'folk', 'happy'],
            'description': 'This is test',
            'youtube_id': 'hQVTIJBZook'
        }

        metadata_dict = {
            'description': 'This is a test song.',
            'view_count': 100,
            'like_count': 10,
            'dislike_count': 1,
            'thumbnail_url': 'http://example.com',
            'tags': ['something', 'test']
        }

        expected_result = {
            'song_number': 12345,
            'release_date': '12/30/2016',
            'title': 'Test Song',
            'url': 'https://youtu.be/hQVTIJBZook',
            'download_url': 'http://downlo.ad/12345',
            'youtube_id': 'hQVTIJBZook',
            'description': 'This is a test song.',
            'view_count': 100,
            'like_count': 10,
            'dislike_count': 1,
            'thumbnail_url': 'http://example.com',
            'tags': ['fun', 'folk', 'happy', 'something', 'test']
        }

        result = fetch_songs.update_song_with_metadata_dict(
            song, metadata_dict)

        self.assertEqual(result, expected_result)

    def test_song_metadata_from_youtube_video_item_returns_valid_metadata_dict(self):
        example_yt_id = 'hQVTIJBZook'
        example_video_item = None

        try:
            api = yapi.YoutubeAPI(settings.YOUTUBE_API_KEY)
            example_video_item = api.get_video_info(example_yt_id).items[0]
        except AttributeError as e:
            raise Exception(
                'Unable to query Youtube API. Possibly over quota.')

        result = fetch_songs.song_metadata_from_youtube_video_item(
            example_video_item)
        self.assertEqual(result['youtube_id'], example_yt_id)
