from django.db import models
from django.core.validators import MinLengthValidator


class Tag(models.Model):
    text = models.CharField(max_length=255, unique=True, validators=[MinLengthValidator(2)])

    def __str__(self):
        return self.text


class Song(models.Model):
    title = models.CharField(max_length=255, validators=[MinLengthValidator(2)])
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, validators=[MinLengthValidator(4)])
    view_count = models.IntegerField(null=True, blank=True)
    like_count = models.IntegerField(null=True, blank=True)
    dislike_count = models.IntegerField(null=True, blank=True)
    song_number = models.IntegerField()
    thumbnail_url = models.CharField(blank=True, null=True, max_length=255)
    release_date = models.DateField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return str(self.song_number) + ' ' + self.title
