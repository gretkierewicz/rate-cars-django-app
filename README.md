# rate_cars

Simple REST API for creating and rating car models.\
Car make and model existence checked with third-party REST API.

### Deployed at Heroku platform: [link](https://tranquil-caverns-25726.herokuapp.com/)

---

## Deployment

Setting up (needs 
[git](https://git-scm.com/downloads),
[docker](https://docs.docker.com/compose/install/) and
[heroku](https://devcenter.heroku.com/articles/heroku-cli) clients installed +
heroku (free) [account registered](https://signup.heroku.com)):

```shell
# tested with Windows' PoweShell

# create folder for project
mkdir rate_cars
cd rate_cars

# get copy of the application's files
git clone https://github.com/gretkierewicz/rate_cars.git .
# there is empty .env file in repo to make building container strait-forward

# pre-build app with docker-compose
docker-compose build

# login with heroku and create app for deployment
heroku login
heroku create
# login to container
heroku container:login

# if you would like to push container to different app
# at end of each next command add: -a full_app_name

# create postgresql DB (this creates DATABASE_URL env variable as well)
heroku addons:create heroku-postgresql:hobby-dev

# push and release container
heroku container:push web
heroku container:release web

# create DB tables for cars app
heroku run python manage.py migrate cars

# start app in web-browser
heroku open

# Enjoy!
```
---

## Assumptions

### Endpoints

```
/cars/ -> post new car
/cars/popular/ -> list 5 most rated car models
/cars/{car_make}
/cars/{car_make}/models/
/cars/{car_make}/models/{model_name}
/cars/{car_make}/models/{model_name}/rate/{rate_value} -> post rate
```
---

### Tests

* Valid data/url kwargs:
  * GET for all endpoints
  * POST for /cars and /rate
* Invalid data/url kwargs:
  * GET for endpoints with kwargs
  * POST for /cars and /rate

---

### Setup

* Containerization with [docker-compose](https://docs.docker.com/compose/)
* Running app with [heroku](https://heroku.com/)

---

## Tech stack

* [Django framework](https://www.djangoproject.com)
* [Django REST framework](https://www.django-rest-framework.org)
* [Django Nested Routers](https://github.com/alanjds/drf-nested-routers) - nice package for creating nested resources

## Sources of knowledge / heplpfull links

* [Deploying Django to Heroku With Docker by Michael Herman](https://testdriven.io/blog/deploying-django-to-heroku-with-docker/)
* [Django query-sets - annotate()](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#annotate)
* [docker-compose with django - docs](https://docs.docker.com/compose/django/)


- [heroku: Container Registry & Runtime (Docker Deploys)](https://devcenter.heroku.com/articles/container-registry-and-runtime)
- [heroku: Django and Static Assets article (whitenoise)](https://devcenter.heroku.com/articles/django-assets)
- [heroku: Local Development with Docker Compose](https://devcenter.heroku.com/articles/local-development-with-docker-compose)


* [StackOverFlow: nice solution with get_random_secret_key()](https://stackoverflow.com/questions/59719175/where-to-run-collectstatic-when-deploying-django-app-to-heroku-using-docker)
    ```shell
    SECRET_KEY = os.environ.get('SECRET_KEY', default=get_random_secret_key())
    ```
* [StackOverFlow: tip for local container update with a cleanup:](https://stackoverflow.com/questions/49316462/how-to-update-existing-images-with-docker-compose)
    ```shell
    docker-compose up --force-recreate --build -d
    docker image prune -f
    ```
* [StackOverFlow: providing DB migrations in local container:](https://stackoverflow.com/questions/33992867/how-do-you-perform-django-database-migrations-when-using-docker-compose)
    ```shell
    #assume django in container named web
    docker-compose run web python3 manage.py migrate
    ```
