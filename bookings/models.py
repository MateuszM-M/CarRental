from django.db import models
from django.contrib.auth.models import User
from cars.models import Car


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    booking_start = models.DateField()
    booking_end = models.DateField()