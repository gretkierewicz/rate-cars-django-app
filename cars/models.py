from django.db import models


class Cars(models.Model):
    class Meta:
        unique_together = ['car_make', 'model_name']

    car_make = models.CharField(max_length=64)
    model_name = models.CharField(max_length=64)
