from django.contrib import admin
from .models import Song, Tag


class SongAdmin(admin.ModelAdmin):
    list_display = ['song_number', 'title', 'release_date']
    list_filter = ['release_date']
    date_hierarchy = 'release_date'
    ordering = ['-song_number']
    search_fields = ['title', 'description']


admin.site.register(Song, SongAdmin)
admin.site.register(Tag)
