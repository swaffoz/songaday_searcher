from django.db import models


class Tag(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Song(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=255)
    view_count = models.IntegerField(null=True)
    like_count = models.IntegerField(null=True)
    dislike_count = models.IntegerField(null=True)
    song_number = models.IntegerField()
    thumbnail_url = models.CharField(blank=True, null=True, max_length=255)
    release_date = models.DateField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return str(self.song_number) + ' ' + self.title
