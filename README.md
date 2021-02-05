# rate_cars

**rate_cars** - simple REST API for rating car models

Deployed at: [Heroku platform](https://tranquil-caverns-25726.herokuapp.com/)

---

## Deployment

Setting up (needs 
[git](https://git-scm.com/downloads),
[docker](https://docs.docker.com/compose/install/) and
[heroku](https://devcenter.heroku.com/articles/heroku-cli) clients installed +
heroku (free) [account registered](https://signup.heroku.com)):

```bash
# create folder for project
mkdir rate_cars
cd rate_cars

# get copy of the application's repo
git clone https://github.com/gretkierewicz/rate_cars.git .

# pre-build app with docker-compose
docker-compose build

# if not yet done - login with heroku and create app for deployment
heroku login
heroku create
# if this is not the only heroku app you have (list apps with 'heroku apps' command)
# at end of each next command add: -a full_app_name
# app name is listed after creating it and has format 'word-word-number'

# create postgresql DB
# this creates DATABASE_URL env variable as well (settings > DATABASE_URL)
heroku addons:create heroku-postgresql:hobby-dev

# push and release container
heroku container:push web
heroku container:release web

# create DB tables
heroku run python manage.py migrate

# start app in web-browser
heroku open
```
---

## Assumptions

* ### Endpoints

```
/cars/ -> post new car
/cars/popular/ -> list 5 most rated car models
/cars/{car_make}
/cars/{car_make}/models/
/cars/{car_make}/models/{model_name}
/cars/{car_make}/models/{model_name}/rate/{rate_value} -> post rate
```
---

* ### Tests

    * TBD

---

* ### Setup

    * Containerization with [docker-compose](https://docs.docker.com/compose/)
    * Running app with [heroku](https://heroku.com/)

---

## Tech stack

* [Django framework](https://www.djangoproject.com)
* [Django REST framework](https://www.django-rest-framework.org)
* [Django Nested Routers](https://github.com/alanjds/drf-nested-routers) - nice package for creating nested resources

## Used sources of knowledge

* [Deploying Django to Heroku With Docker by Michael Herman](https://testdriven.io/blog/deploying-django-to-heroku-with-docker/)


* [docker-compose with django - docs](https://docs.docker.com/compose/django/)


* [heroku: Container Registry & Runtime (Docker Deploys)](https://devcenter.heroku.com/articles/container-registry-and-runtime)
* [heroku: Django and Static Assets article (whitenoise)](https://devcenter.heroku.com/articles/django-assets)
* [heroku: Local Development with Docker Compose](https://devcenter.heroku.com/articles/local-development-with-docker-compose)


* [StackOverFlow: nice solution with get_random_secret_key()](https://stackoverflow.com/questions/59719175/where-to-run-collectstatic-when-deploying-django-app-to-heroku-using-docker)
    ```python
    SECRET_KEY = os.environ.get('SECRET_KEY', default=get_random_secret_key())
    ```
* [StackOverFlow: good guide for local container update:](https://stackoverflow.com/questions/49316462/how-to-update-existing-images-with-docker-compose)
    ```shell
    docker-compose up --force-recreate --build -d
    docker image prune -f
    ```
* [StackOverFlow: how to provide DB migrations in local container:](https://stackoverflow.com/questions/33992867/how-do-you-perform-django-database-migrations-when-using-docker-compose)
    ```shell
    #assume django in container named web
    docker-compose run web python3 manage.py migrate
    ```
* [Django query-sets - annotate()](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#annotate)
