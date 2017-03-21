Song A Day Searcher Deployment
==============================

To deploy the app to the server you need to:

1. [Set the necessary environment variables](#environment).
2. [Add any SSH Keys you want to use to the server](#ssh-keys).
3. [Run the Start Provision fabric script, if the server is new](#provisioning).
4. [Run the Deploy script](#deploying).

* * *


## Environment
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

- You can get your very own Youtube API Key [here](https://console.developers.google.com/) if you need one.

* * *


## SSH Keys

If there are any new SSH public keys you want to add to the server, you can put them in the `deploy/ssh-keys` directory. The provisioning script will throw them up to the server.


* * *


## Provisioning

Provisioning only needs to be done once on new servers.
Run the provisioning script via:

```
fab -f deploy/fabfile.py start_provision
```

* * *


## Deploying

If a server has been provisioned and the environment variables are set, you can run the deployment script via:
 
```
sh deploy_production.sh
```