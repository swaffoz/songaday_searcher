Song A Day Searcher
===================

Built with ❤️ and [Django](https://www.djangoproject.com) in Kansas.

A running instance is available [here](http://159.203.165.95/).

API documentation available  [here](https://github.com/zaneswafford/songaday_searcher/blob/master/API.md).

Deploy documentation available  [here](https://github.com/zaneswafford/songaday_searcher/blob/master/DEPLOY.md).

* * *

Install dependencies via:
`pip install -r requirements.txt`

Run via:
`python manage.py runserver`

Run the background song fetcher via:
```
celery -A songaday_searcher beat -l info
celery -A songaday_searcher worker -l info
```

Run tests via:
`python manage.py test`

- Requires instances of the following running locally:
    - PostGreSQL
    - Redis

- The Following environment variables must be set:
    - `DJANGO_SECRET_KEY`
    - `DJANGO_DATABASE_NAME`
    - `DJANGO_DATABASE_USER`
    - `DJANGO_DATABASE_PASSWORD`
    - `YOUTUBE_API_KEY`

- You can set them in Bash via:
```
export DJANGO_SECRET_KEY='some long secret that only you know'
export DJANGO_DATABASE_NAME='postgres database name'
export DJANGO_DATABASE_USER='postgres database username'
export DJANGO_DATABASE_PASSWORD='password for postgres database user'
export YOUTUBE_API_KEY='Your youtube api key'
```

- You can get your very own Youtube API Key [here](https://console.developers.google.com/).
