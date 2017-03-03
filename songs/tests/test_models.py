import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from songs.models import Song, Tag


class SongModelTestCase(TestCase):

    def test_empty_songs_cannot_save(self):
        """
        Songs must have the song_number and release_date fields filled in.
        """
        with self.assertRaises(IntegrityError):
            Song.objects.create()

    def test_song_with_short_title_is_invalid(self):
        """
        Songs should have a title of 2 characters or more. Any less is invalid.
        """
        song_number = 0
        title = 'a'
        url = 'https://zaneswafford.com/'
        release_date = datetime.date.today()

        song = Song.objects.create(song_number=song_number,
                                   title=title,
                                   url=url,
                                   release_date=release_date)

        with self.assertRaises(ValidationError):
            song.clean_fields()

    def test_song_with_short_url_is_invalid(self):
        """
        Songs should have a url of 4 characters or more. Any less is invalid.
        """
        song_number = 1
        title = 'My Song'
        url = 'htt'
        release_date = datetime.date.today()

        song = Song.objects.create(song_number=song_number,
                                   title=title,
                                   url=url,
                                   release_date=release_date)

        with self.assertRaises(ValidationError):
            song.clean_fields()

    def test_valid_song_does_save(self):
        """
        Saving a Song with appropriate data should succeed and have clean fields.
        """
        song_number = 1
        title = 'My Song'
        description = 'This is my song'
        url = 'https://zaneswafford.com/'
        release_date = datetime.date.today()
        view_count = 987
        like_count = 654
        dislike_count = 321
        thumbnail_url = 'https://otters.io/'
        tag = Tag.objects.create(text='mytag')

        song = Song.objects.create(song_number=song_number,
                                   title=title,
                                   description=description,
                                   url=url,
                                   release_date=release_date,
                                   view_count=view_count,
                                   like_count=like_count,
                                   dislike_count=dislike_count,
                                   thumbnail_url=thumbnail_url)
        song.tags.add(tag)
        song.save()
        song.clean_fields()

    def test_song_string_representation(self):
        """
        A Song should show its song number and title in its string representation.
        """
        song_number = 1
        title = 'My Song'
        url = 'https://zaneswafford.com/'
        release_date = datetime.date.today()

        song = Song.objects.create(song_number=song_number,
                                   title=title,
                                   url=url,
                                   release_date=release_date)

        self.assertIn(str(song.song_number), str(song))
        self.assertIn(str(song.title), str(song))


class TagModelTestCase(TestCase):

    def test_tag_with_short_text_is_invalid(self):
        """
        Tags should have a text of 2 characters or more. Any less is invalid.
        """
        text = "T"
        tag = Tag.objects.create(text=text)

        with self.assertRaises(ValidationError):
            tag.clean_fields()

    def test_tags_must_be_unique(self):
        """
        Tag objects must have unique text. 
        Two tags cannot be the same.
        """
        with self.assertRaises(IntegrityError):
            text = "mytag"
            Tag.objects.create(text=text)
            Tag.objects.create(text=text)

    def test_tag_string_representation(self):
        """
        A Tag should show its text in its string representation.
        """
        text = "mytag"
        tag = Tag.objects.create(text=text)

        self.assertIn(str(tag.text), str(tag))
