from django.db import models
from django.core.validators import MinLengthValidator


class TagManager(models.Manager):

    def get_by_natural_key(self, id, text):
        return self.get(id=id)


class Tag(models.Model):
    objects = TagManager()

    text = models.CharField(max_length=255, unique=True,
                            validators=[MinLengthValidator(2)])

    # Natural key has to be a tuple for deserialization to work.
    # This is the most logical tuple I could come up with. I wish we could use
    # only text.
    def natural_key(self):
        return (self.id, self.text)

    def __str__(self):
        return self.text


class Song(models.Model):
    title = models.CharField(max_length=255, validators=[
                             MinLengthValidator(2)])
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, validators=[MinLengthValidator(4)])
    download_url = models.CharField(max_length=255, null=True, blank=True)
    view_count = models.IntegerField(null=True, blank=True)
    like_count = models.IntegerField(null=True, blank=True)
    dislike_count = models.IntegerField(null=True, blank=True)
    song_number = models.IntegerField()
    thumbnail_url = models.CharField(blank=True, null=True, max_length=255)
    release_date = models.DateField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return str(self.song_number) + ' ' + self.title


class SongUpdateToken(models.Model):
    started = models.DateTimeField()
    finished = models.DateTimeField(null=True, blank=True)
    song_count = models.IntegerField(null=True)

    def __str__(self):
        return ('started: ' + str(self.started) + '; ' +
                'finished: ' + str(self.finished))
