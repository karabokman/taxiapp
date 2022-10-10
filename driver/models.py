from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Taxi(models.Model):
    no_plate = models.CharField(max_length=255, unique=True)
    model = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    seats = models.IntegerField()
    def __str__(self):
        return self.no_plate

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver_no = models.CharField(max_length=255, unique=True)
    img = models.ImageField(upload_to='d_img', default='placeholder.jpeg')
    contacts = models.CharField(max_length=255)
    taxi = models.ForeignKey(Taxi,null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.driver_no


class Destination(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

