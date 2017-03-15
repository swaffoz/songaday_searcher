import json
import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.core import serializers
from django.test.utils import override_settings

from songs.models import Song, Tag, SongUpdateToken
from songs import views


# Disable caches during tests. We don't need caches where we're going.
@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        },
    },
)

class SongViewTestCase(TestCase):

    fixtures = ['songs.yaml', 'tags.yaml', 'songupdatetokens.yaml']

    def setUp(self):
        # Create a fake song for today
        Song.objects.create(song_number=777, title="Today's song!",
                            description="This is today's song!", release_date=datetime.date.today())

    def test_index_returns_200_ok(self):
        """
        Index view should return a 200 OK response to requests
        """
        index_url = reverse('index')
        response = Client().get(index_url)

        self.assertEqual(response.status_code, 200)

    def test_index_returns_help_message(self):
        """
        Index view should return a help message
        """
        index_url = reverse('index')
        response = Client().get(index_url)
        message = json.loads(response.content)

        self.assertTrue('help' in message)

    def test_blank_search_returns_nothing(self):
        """
        Search view should return nothing if no search terms are provided
        """
        search_url = reverse('search', kwargs={'text': None})
        response = Client().get(search_url)

        self.assertTrue(len(response.content) == 0)

    def test_search_returns_matching_songs(self):
        """
        Search view should return matching songs that fuzzy match to text
        """
        expected_result = Song.objects.get(title='Dog Theme #9874')
        search_term = 'dog'
        search_url = reverse('search', kwargs={'text': search_term})
        response = Client().get(search_url)

        contains_expected_result = False
        for result in serializers.deserialize("json", response.content):
            if result.object == expected_result:
                contains_expected_result = True

        self.assertTrue(contains_expected_result)

    def test_search_does_not_return_nonmatching_songs(self):
        """
        Search view should not return songs that do not match to text
        """
        unexpected_results = Song.objects.exclude(title='Dog Theme #9874')

        search_term = 'dog'
        search_url = reverse('search', kwargs={'text': search_term})
        response = Client().get(search_url)

        contains_unexpected_result = False
        for result in serializers.deserialize("json", response.content):
            if result.object in unexpected_results:
                contains_unexpected_result = True

        self.assertFalse(contains_unexpected_result)

    def test_tags_returns_200_ok(self):
        """
        Tags view should return a 200 OK response to requests
        """
        tags_url = reverse('tags')
        response = Client().get(tags_url)

        self.assertEqual(response.status_code, 200)

    def test_tags_returns_all_tags_if_none_specified(self):
        """
        Tags view should return all available tags if tag isn't specified
        """
        tags_url = reverse('tags')
        response = Client().get(tags_url)

        expected_results = Tag.objects.all()
        contains_unexpected_result = False
        for result in serializers.deserialize("json", response.content):
            if result.object not in expected_results:
                contains_unexpected_result = True

        self.assertFalse(contains_unexpected_result)

    def test_tags_returns_matching_songs(self):
        """
        Tags view should return songs that contain the specified tag
        """
        tag_id = 3
        tag_text = 'dogs'
        tag_url = reverse('tag', kwargs={'text': tag_text})
        response = Client().get(tag_url)

        expected_result = Song.objects.get(tags__in=[tag_id])
        contains_expected_result = False
        for result in serializers.deserialize("json", response.content):
            if result.object == expected_result:
                contains_expected_result = True

        self.assertTrue(contains_expected_result)

    def test_tags_does_not_return_nonmatching_songs(self):
        """
        Tags view should not return songs that don't contain the specified tag
        """
        tag_id = 3
        tag_text = 'dogs'
        tag_url = reverse('tag', kwargs={'text': tag_text})
        response = Client().get(tag_url)

        unexpected_results = Song.objects.exclude(tags__in=[tag_id])
        contains_unexpected_result = False
        for result in serializers.deserialize("json", response.content):
            if result.object in unexpected_results:
                contains_unexpected_result = True

        self.assertFalse(contains_unexpected_result)

    def test_today_returns_200_ok(self):
        """
        Today view should return a 200 OK response to requests
        """
        today_url = reverse('today')
        response = Client().get(today_url)

        self.assertEqual(response.status_code, 200)

    def test_today_returns_todays_song(self):
        """
        Today view should return a single song for today
        """
        today_url = reverse('today')
        response = Client().get(today_url)

        expected_result = Song.objects.get(release_date=datetime.date.today())
        contains_expected_result = False

        for result in serializers.deserialize("json", response.content):
            if result.object == expected_result:
                contains_expected_result = True

        self.assertTrue(contains_expected_result)

    def test_latest_returns_200_ok(self):
        """
        Latest view should return a 200 OK response to requests
        """
        latest_url = reverse('latest')
        response = Client().get(latest_url)

        self.assertEqual(response.status_code, 200)

    def test_latest_returns_todays_song(self):
        """
        Latest view should return a single song with latest release_date
        """
        latest_url = reverse('latest')
        response = Client().get(latest_url)

        expected_result = Song.objects.order_by('-release_date')[0]
        contains_expected_result = False

        for result in serializers.deserialize("json", response.content):
            if result.object == expected_result:
                contains_expected_result = True

        self.assertTrue(contains_expected_result)

    def test_date_returns_song_for_date(self):
        """
        Date view should return a single song for the date provided
        """
        test_date = datetime.date(2017, 2, 27)
        date_url = reverse('from_date', kwargs={
                           'month': test_date.month,
                           'day': test_date.day,
                           'year': test_date.year})

        response = Client().get(date_url)
        expected_result = Song.objects.get(release_date=test_date)
        contains_expected_result = False

        for result in serializers.deserialize("json", response.content):
            if result.object == expected_result:
                contains_expected_result = True

        self.assertTrue(contains_expected_result)

    def test_songs_returns_200_ok(self):
        """
        Songs view should return a 200 OK response to requests
        """
        songs_url = reverse('songs')
        response = Client().get(songs_url)

        self.assertEqual(response.status_code, 200)

    def test_songs_returns_all_songs_if_none_specified(self):
        """
        Songs view should return all songs if none is specified
        """
        songs_url = reverse('songs')
        response = Client().get(songs_url)

        remaining_songs = list(Song.objects.all())
        for result in serializers.deserialize("json", response.content):
            if result.object in remaining_songs:
                remaining_songs.remove(result.object)

        self.assertEqual(len(remaining_songs), 0)

    def test_songs_returns_song_for_number(self):
        """
        Songs view should return a single song for the song number provided
        """
        song_number = 9876
        songs_url = reverse('song', kwargs={'number': song_number})
        response = Client().get(songs_url)

        expected_result = Song.objects.get(song_number=song_number)
        contains_expected_result = False

        for result in serializers.deserialize("json", response.content):
            if result.object == expected_result:
                contains_expected_result = True

        self.assertTrue(contains_expected_result)

    def test_last_updated_returns_token(self):
        """
        Last Updated view should return a token with last update to songs
        """
        last_updated_url = reverse('last_updated')
        response = Client().get(last_updated_url)

        expected_token = SongUpdateToken.objects.get(pk=1)
        expected_dict = {'started': str(expected_token.started),
                         'finished': str(expected_token.finished),
                         'songs_updated': expected_token.song_count}
        expected_result = json.dumps(expected_dict)

        self.assertTrue(expected_result in str(response.content))
