from django.db import models


class Cars(models.Model):
    class Meta:
        ordering = 'make',

    make = models.CharField(max_length=72, unique=True)

    def __str__(self):
        return self.make


class CarModels(models.Model):
    class Meta:
        ordering = 'car_make', 'name',
        unique_together = ['name', 'car_make']

    name = models.CharField(max_length=136)
    car_make = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='models')
