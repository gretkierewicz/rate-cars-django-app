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
# if this is not your only heroku app (check with 'heroku apps' command)
# at end of each next line add: -a full_app_name
# app name is listed after creating and has format 'word-word-number'

# setup at least SECRET_KEY env variable (not necessary, but recomended)
heroku config:set SECRET_KEY=type_in_your_secret_key_here

# push and release container
heroku container:push web
heroku container:release web

# start app in web-browser
heroku open
```
---

## Assumptions

* ### Endpoints

    * POST /cars
        * [ ] Request body should contain car make and model name
        * [ ] Based on this data, its existence should be checked here https://vpic.nhtsa.dot.gov/api/
        * [ ] If the car doesn't exist - return an error
        * [ ] If the car exists - it should be saved in the database

    * POST /rate
        * [ ] Add a rate for a car from 1 to 5
    
    * GET /cars
        * [ ] Should fetch list of all cars already present in application database with their current average rate
    
    * GET /popular
        * [ ] Should return top cars already present in the database ranking based on number of rates

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