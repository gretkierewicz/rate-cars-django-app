from django.db import models


class Cars(models.Model):
    car_make = models.CharField(max_length=64)
    model_name = models.CharField(max_length=64)
