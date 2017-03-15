Song A Day Searcher API
=======================

- [Index](#index)
- [Search](#search)
- [Songs](#songs)
    - [All Songs](#songs)
    - [Song With Number](#song-with-number)
    - [Song From Date](#song-from-date)
    - [Song For Today](#song-for-today)
    - [Latest Song](#latest-song)
- [Tags](#tags)
    - [All Tags](#tags)
    - [Songs With Tag](#songs-with-tag)
- [Last Updated](#last-updated)

* * *

## Index
Returns an object with a link to this documentation.

### URL: `/`
### Method: `GET`
### Example Response:
```
{
  "help": "See API documentation here: https://github.com/zaneswafford/songaday_searcher/blob/master/API.md"
}
```

* * *

## Search
Returns an array of songs that match a provided string. The songs are matched by PostgreSQL’s trigram search and do not have to be exact. 

### URL: `/search/<text>`
### Method: `GET`
### Example Response (shortened):
```
[{
"model": "songs.song",
"pk": 12345678,
"fields": {
  "title": "A Song About Dogs",
  "description": "This is a song about dogs",
  "url": "https://youtu.be/abcdefghijk",
  "download_url": "https://jonathanmann.bandcamp.com/track/dog-song",
  "view_count": 1234,
  "like_count": 123,
  "dislike_count": 1,
  "song_number": 98765,
  "thumbnail_url": "https://i.ytimg.com/vi/abcdefghijk/default.jpg",
  "release_date": "2017-03-15",
  "tags": [
    [
      9876,
      "dogs"
    ]
  ]
}
}]
```

* * *

## Songs
Returns an array of all songs. 

**Warning!** This will return a large dump of data.

### URL: `/songs`
### Method: `GET`
### Example Response (shortened):
```
[{
"model": "songs.song",
"pk": 12345678,
"fields": {
  "title": "A Song About Dogs",
  "description": "This is a song about dogs",
  "url": "https://youtu.be/abcdefghijk",
  "download_url": "https://jonathanmann.bandcamp.com/track/dog-song",
  "view_count": 1234,
  "like_count": 123,
  "dislike_count": 1,
  "song_number": 98765,
  "thumbnail_url": "https://i.ytimg.com/vi/abcdefghijk/default.jpg",
  "release_date": "2017-03-15",
  "tags": [
    [
      9876,
      "dogs"
    ]
  ]
}
}]
```

* * *

## Song With Number
Returns a single song with the given number

### URL: `/song/<number>`
### Method: `GET`
### Example Response:

```
[{
"model": "songs.song",
"pk": 12345678,
"fields": {
  "title": "A Song About Dogs",
  "description": "This is a song about dogs",
  "url": "https://youtu.be/abcdefghijk",
  "download_url": "https://jonathanmann.bandcamp.com/track/dog-song",
  "view_count": 1234,
  "like_count": 123,
  "dislike_count": 1,
  "song_number": 98765,
  "thumbnail_url": "https://i.ytimg.com/vi/abcdefghijk/default.jpg",
  "release_date": "2017-03-15",
  "tags": [
    [
      9876,
      "dogs"
    ]
  ]
}
}]
```

* * *

## Song From Date
Returns a single song with the given date

### URL: `/from/<month>/<day>/<year>`
### Method: `GET`
### Example Response:

```
[{
"model": "songs.song",
"pk": 12345678,
"fields": {
  "title": "A Song About Dogs",
  "description": "This is a song about dogs",
  "url": "https://youtu.be/abcdefghijk",
  "download_url": "https://jonathanmann.bandcamp.com/track/dog-song",
  "view_count": 1234,
  "like_count": 123,
  "dislike_count": 1,
  "song_number": 98765,
  "thumbnail_url": "https://i.ytimg.com/vi/abcdefghijk/default.jpg",
  "release_date": "2017-03-15",
  "tags": [
    [
      9876,
      "dogs"
    ]
  ]
}
}]
```

* * *

## Song For Today
Returns a single song for today. Server date in Eastern Standard Time UTC-05:00. Will return 404 if there is no song with a release date of today in the spreadsheet. To always get the latest song, see [Latest Song](#latest-song)

### URL: `/today`
### Method: `GET`
- Example Response:
```
[{
"model": "songs.song",
"pk": 12345678,
"fields": {
  "title": "A Song About Dogs",
  "description": "This is a song about dogs",
  "url": "https://youtu.be/abcdefghijk",
  "download_url": "https://jonathanmann.bandcamp.com/track/dog-song",
  "view_count": 1234,
  "like_count": 123,
  "dislike_count": 1,
  "song_number": 98765,
  "thumbnail_url": "https://i.ytimg.com/vi/abcdefghijk/default.jpg",
  "release_date": "2017-03-15",
  "tags": [
    [
      9876,
      "dogs"
    ]
  ]
}
}]
```

* * *

## Latest Song
Returns the latest song. May be different than the [Song For Today](#song-for-today) if, for example, the songs spreadsheet has not been updated in a while.

### URL: `/latest`
### Method: `GET`
- Example Response:
```
[{
"model": "songs.song",
"pk": 12345678,
"fields": {
  "title": "A Song About Dogs",
  "description": "This is a song about dogs",
  "url": "https://youtu.be/abcdefghijk",
  "download_url": "https://jonathanmann.bandcamp.com/track/dog-song",
  "view_count": 1234,
  "like_count": 123,
  "dislike_count": 1,
  "song_number": 98765,
  "thumbnail_url": "https://i.ytimg.com/vi/abcdefghijk/default.jpg",
  "release_date": "2017-03-15",
  "tags": [
    [
      9876,
      "dogs"
    ]
  ]
}
}]
```

* * *

## Tags
Returns an array of all available tags. 

**Warning!** This will return a large dump of data.

### URL: `/tags`
### Method: `GET`
### Example Response (shortened):
```
[
  {
    "model": "songs.tag",
    "pk": 9876,
    "fields": {
      "text": "dogs"
    }
  },
  {
    "model": "songs.tag",
    "pk": 9877,
    "fields": {
      "text": "cats"
    }
  }
]
```

* * *

## Songs With Tag
Returns an array of songs with the provided tag

### URL: `/tags/<text>`
### Method: `GET`
### Example Response (shortened):
```
[{
"model": "songs.song",
"pk": 12345678,
"fields": {
  "title": "A Song About Dogs",
  "description": "This is a song about dogs",
  "url": "https://youtu.be/abcdefghijk",
  "download_url": "https://jonathanmann.bandcamp.com/track/dog-song",
  "view_count": 1234,
  "like_count": 123,
  "dislike_count": 1,
  "song_number": 98765,
  "thumbnail_url": "https://i.ytimg.com/vi/abcdefghijk/default.jpg",
  "release_date": "2017-03-15",
  "tags": [
    [
      9876,
      "dogs"
    ]
  ]
}
}]
```

* * *

## Last Updated
Returns a token with information about the last time songs were fetched from the canonical spreadsheet and Youtube. 

### URL: `/lastupdated`
### Method: `GET`
### Example Response:
```
{
  "started": "2017-03-15 06:30:00.012345+00:00",
  "finished": "2017-03-15 06:33:00.987654+00:00",
  "songs_updated": 4321
}
```

* * *
